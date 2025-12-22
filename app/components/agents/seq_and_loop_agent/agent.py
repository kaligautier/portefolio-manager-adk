"""
Story Refinement Pipeline - LoopAgent Pattern Example.

Ce fichier démontre l'utilisation de LoopAgent et SequentialAgent pour créer un pipeline
de raffinement itératif d'histoires avec critique et amélioration.

## Architecture Multi-Agents

**Pipeline global (SequentialAgent):**
1. InitialWriterAgent → Écrit le premier draft
2. StoryRefinementLoop → Boucle de raffinement (LoopAgent)

**Boucle de raffinement (LoopAgent):**
1. CriticAgent → Évalue l'histoire et fournit une critique
2. RefinerAgent → Améliore l'histoire OU appelle exit_loop() si approuvée

## Pattern LoopAgent

Le LoopAgent exécute ses sub-agents en boucle jusqu'à ce que:
- Un agent appelle un outil qui break la boucle (exit_loop())
- Le nombre max d'itérations est atteint (max_iterations)

## Flux de données (output_key)

Les agents communiquent via le state partagé avec output_key:
- InitialWriterAgent: output_key="current_story" → Crée l'histoire initiale
- CriticAgent: output_key="critique" → Génère la critique
- RefinerAgent: output_key="current_story" → Met à jour l'histoire raffinée

Dans les instructions, utilisez {current_story} et {critique} pour accéder au state.

## Exit Loop Strategy

Le RefinerAgent a un outil exit_loop() qui permet de sortir de la boucle:
- Si critique == "APPROVED" → Appelle exit_loop() → Break la boucle
- Sinon → Rafine l'histoire → Continue la boucle (prochain tour: CriticAgent)
"""

import logging

from google.adk.agents import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.tools.function_tool import FunctionTool
from google.adk.agents.sequential_agent import SequentialAgent

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool

from app.config.settings import settings

logger = logging.getLogger(__name__)

# ============================================================================
# Exit Loop Tool
# ============================================================================
# Cet outil permet au RefinerAgent de sortir de la boucle de raffinement
# quand l'histoire est approuvée par le CriticAgent.
def exit_loop():
    """
    Appeler cette fonction UNIQUEMENT quand la critique est 'APPROVED'.
    Indique que l'histoire est terminée et qu'aucune autre modification n'est nécessaire.
    """
    return {"status": "approved", "message": "Histoire approuvée. Sortie de la boucle de raffinement."}


# ============================================================================
# Agent 1: Initial Writer - Crée le premier draft
# ============================================================================
# Cet agent démarre le pipeline en écrivant la première version de l'histoire.
# output_key="current_story" → Stocke l'histoire dans le state partagé.
initial_writer_agent = LlmAgent(
    name="InitialWriterAgent",
    model=settings.MODEL,
    instruction="""En te basant sur la demande de l'utilisateur, écris le premier draft d'une courte histoire (environ 100-150 mots).
    Retourne uniquement le texte de l'histoire, sans introduction ni explication.""",
    output_key="current_story",
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)

# ============================================================================
# Agent 2: Refiner - Améliore l'histoire basé sur la critique
# ============================================================================
# Cet agent analyse la critique et décide:
# - Si "APPROVED" → Appelle exit_loop() pour sortir de la boucle
# - Sinon → Rafine l'histoire en intégrant les feedbacks
#
# IMPORTANT:
# - Accède à {current_story} et {critique} depuis le state partagé
# - output_key="current_story" → Écrase l'histoire avec la version raffinée
# - L'outil exit_loop() permet de break la LoopAgent
refiner_agent = LlmAgent(
    name="RefinerAgent",
    model=settings.MODEL,
    instruction="""Tu es un raffineur d'histoires. Tu as accès au draft de l'histoire et à la critique.

    Draft de l'histoire: {current_story}
    Critique: {critique}

    Ta tâche est d'analyser la critique.
    - SI la critique est EXACTEMENT "APPROVED", tu DOIS appeler la fonction `exit_loop` et rien d'autre.
    - SINON, réécris l'histoire pour incorporer pleinement les feedbacks de la critique.""",
    output_key="current_story",  # Écrase l'histoire avec la nouvelle version raffinée
    tools=[
        FunctionTool(exit_loop)
    ],  # L'outil est initialisé avec la référence de fonction
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)

# ============================================================================
# Agent 3: Critic - Évalue la qualité de l'histoire
# ============================================================================
# Cet agent fournit une critique constructive de l'histoire:
# - Si l'histoire est bonne → Retourne "APPROVED"
# - Sinon → Fournit 2-3 suggestions d'amélioration
#
# output_key="critique" → Stocke la critique dans le state pour le RefinerAgent
critic_agent = LlmAgent(
    name="CriticAgent",
    model=settings.MODEL,
    instruction="""Tu es un critique d'histoires constructif. Évalue l'histoire fournie ci-dessous.
    Histoire: {current_story}

    Évalue l'intrigue, les personnages et le rythme de l'histoire.
    - Si l'histoire est bien écrite et complète, tu DOIS répondre avec la phrase exacte: "APPROVED"
    - Sinon, fournis 2-3 suggestions spécifiques et actionnables pour l'améliorer.""",
    output_key="critique",  # Stocke le feedback dans le state
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)

# ============================================================================
# LoopAgent: Boucle de raffinement itératif
# ============================================================================
# Le LoopAgent exécute CriticAgent → RefinerAgent en boucle:
# 1. CriticAgent évalue l'histoire et génère une critique
# 2. RefinerAgent améliore l'histoire OU appelle exit_loop() si approuvée
# 3. Retour à l'étape 1 (sauf si exit_loop() est appelé ou max_iterations atteint)
#
# max_iterations=2 → Maximum 2 tours de critique/raffinement
# Si exit_loop() est appelé → La boucle se termine immédiatement
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,
)

# ============================================================================
# SequentialAgent: Pipeline global (Root Agent)
# ============================================================================
# Le SequentialAgent orchestre le workflow complet en séquence:
# 1. InitialWriterAgent → Crée le premier draft
# 2. StoryRefinementLoop → Rafine l'histoire via boucle critique/amélioration
#
# Pas de callbacks ici car c'est un orchestrateur (les callbacks sont sur les LlmAgents)
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
)



