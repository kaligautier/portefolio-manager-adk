## Portfolio Manager Multi-Agents

Gestionnaire de portefeuille multi-agents permettant de passer des ordres sur Interactive Brokers (IBKR), d'analyser son portefeuille, d'évaluer des actions et d'identifier les tendances de marché.

## Le constat 
Actuelement j'utilse le CTO Trade Republic ainsi que le CTO & PEA BoursoBank, les apis pour acheter/vendre et consulter des valeurs est pas facilement utilisable les apis sont fermés pour ce genre d'usage. 

Je souhaîte craquer le sujet en passant d'un usage conversationnel à un workflow agentic automatisé capable analyser les marchés, lire la press, et passer des ordres. 

Pour cela je vais avoir besoin de faire connaître mon niveau de risque et mon profil investisseur. 

Je vais devoir trouver un moyen de déclencher mon workflow. 

## La vision - un gestionnaire de patrimoine autonome agentique 



### Workflow Autonome Quotidien

Le workflow s'exécute automatiquement via l'endpoint `/run/daily` :

1. **Charger la policy** → `investment_policy/default_policy.yaml`
   - Profil investisseur (risk tolerance, horizon)
   - Règles de gestion du risque (max drawdown, stop loss, take profit)
   - Allocation d'actifs cible
   - Stratégies de trading (reinforce winners, sector rotation, cut losers)

2. **Lire IBKR** → `ibkr_reader_agent`
   - Positions actuelles avec quantités et valeurs
   - Cash disponible et buying power
   - PnL réalisé et non réalisé

3. **Lire marché** → `market_reader_agent`
   - Prix en temps réel pour toutes les positions
   - Volatilité 30 jours et niveau VIX
   - Tendances de marché (bull/bear/neutral)
   - Performance sectorielle

4. **Évaluer** → `portfolio_evaluator_agent`
   - Drawdown courant vs max autorisé
   - Concentration par position vs limites
   - Exposition globale vs seuils policy
   - Positions atteignant stop loss ou take profit
   - Drift d'allocation vs cibles

5. **Décider** → `decision_maker_agent`
   - **HOLD** : Aucune action si tout est dans les limites
   - **REINFORCE** : Augmenter positions gagnantes (+20%)
   - **ROTATE** : Changer allocation sectorielle
   - **CUT_LOSERS** : Vendre positions perdantes (-10%)
   - **REBALANCE** : Réajuster allocation cible

6. **Exécuter sur IBKR** → `order_executor_agent`
   - Lookup contract IDs (conid)
   - Preview ordres (WhatIf)
   - Placement ordres avec paramètres policy
   - Capture order IDs et confirmations

7. **Loguer** → Callbacks système
   - Tous les appels d'agents sont loggés
   - Tous les appels d'outils MCP sont tracés
   - Audit trail complet pour conformité

## Déclenchement du Workflow Autonome

### Option 1: Cloud Scheduler (Recommandé - Production)

Configurez Cloud Scheduler pour appeler l'endpoint `/run/daily` automatiquement :

```bash
gcloud scheduler jobs create http daily-portfolio-analysis \
  --location=us-central1 \
  --schedule="0 10 * * 1-5" \
  --uri="https://your-app.run.app/run/daily" \
  --http-method=POST \
  --time-zone="America/New_York" \
  --description="Daily autonomous portfolio management"
```

Cron: `0 10 * * 1-5` = Tous les jours de semaine à 10h (après ouverture des marchés US)

### Option 2: Manuel (Testing)

```bash
# Workflow autonome
curl -X POST https://your-app.run.app/run/daily

# Conversation interactive avec l'agent
curl -X POST https://your-app.run.app/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "portefolio_master_agent",
    "user_id": "user123",
    "session_id": "session456",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Analyse mon portefeuille et recommande des actions"}]
    }
  }'
```

### Option 3: APScheduler (Local)


Pour tester en local, ajoutez dans `application.py` :

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(trigger_daily, 'cron', hour=10, minute=0, day_of_week='mon-fri')
scheduler.start()
```

## Routes API et Interaction avec les Agents

L'application expose plusieurs routes pour interagir avec les agents. Voir [docs/API_ROUTES.md](docs/API_ROUTES.md) pour la documentation complète.

### Routes disponibles

| Route | Méthode | Description |
|-------|---------|-------------|
| `/run` | POST | Conversation synchrone avec un agent |
| `/run/sse` | POST | Conversation avec streaming (Server-Sent Events) |
| `/run/daily` | POST | Déclenche le workflow autonome quotidien |
| `/health` | GET | Health check |
| `/docs` | GET | Documentation Swagger UI |

### Agents disponibles

**Agents root (accessibles via `/run` et `/run/sse`):**
- `portefolio_master_agent` - Orchestrateur du workflow autonome (5 sous-agents)
- `agent_with_vertex_rag` - Agent avec RAG Vertex AI

**Sous-agents (automatiquement exécutés par `portefolio_master_agent`):**
- `ibkr_reader_agent`, `market_reader_agent`, `portfolio_evaluator_agent`, `decision_maker_agent`, `order_executor_agent`

### Exemples d'utilisation

```bash
# 1. Conversation interactive
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "portefolio_master_agent",
    "user_id": "trader1",
    "session_id": "session123",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Quelle est la valeur totale de mon portefeuille?"}]
    }
  }'

# 2. Streaming avec SSE
curl -X POST http://localhost:8080/run/sse \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "app_name": "portefolio_master_agent",
    "user_id": "trader1",
    "session_id": "session123",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Analyse complète avec recommandations"}]
    }
  }'

# 3. Workflow autonome
curl -X POST http://localhost:8080/run/daily
```

## Objectifs

Créer une solution agentique pour l'analyse de patrimoine et l'automatisation de l'investissement en utilisant :
- **IBKR** (Interactive Brokers) : courtier pour l'achat/vente de produits financiers
- **Protocole MCP** : intégration avec IBKR
- **ADK Google** : Kit de Développement d'Agents

## Architecture

### Vue d'ensemble

Le système utilise une architecture multi-conteneurs orchestrée par Docker Compose :

```
┌─────────────────────────────────────────────────────────────┐
│                    Portfolio Manager App                     │
│                      (FastAPI + ADK)                         │
│                        Port: 8080                            │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTP
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                       MCP Server                             │
│              (FastMCP - Streamable HTTP)                     │
│                        Port: 5002                            │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    IBKR API Gateway                          │
│           (Interactive Brokers Client Portal)                │
│                        Port: 5055                            │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
                    ┌─────────────────┐
                    │   IBKR Cloud    │
                    │   (api.ibkr.com)│
                    └─────────────────┘
```

### Flux de communication

1. **Agents ADK** → Appel MCP via `McpToolset(url="http://localhost:5002/mcp")`
2. **MCP Server** → Proxy les requêtes vers le Gateway IBKR (`https://host.docker.internal:5055/v1/api`)
3. **Gateway IBKR** → Communique avec l'API cloud IBKR (`https://api.ibkr.com`)
4. **Réponses** ← Remontent la chaîne jusqu'aux agents

### Services Docker

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `api_gateway` | `ib_mcp_api_gateway:v0.1` | 5055 | Gateway IBKR Client Portal (Java) |
| `mcp_server` | `ib_mcp_mcp_server:v0.1` | 5002 | Serveur MCP avec FastMCP |
| `app` | `portfolio_manager_app:v0.1` | 8080 | Application FastAPI + ADK |

### Démarrage rapide

#### 1. Configuration

Copiez `.env.example` vers `.env` et configurez les variables :

```bash
# IBKR Configuration
IBKR_ACCOUNT_ID=XXX  # Remplacez par votre account ID IBKR

# IBKR Gateway Configuration
GATEWAY_PORT=5055
GATEWAY_ENDPOINT=/v1/api
GATEWAY_INTERNAL_BASE_URL=https://host.docker.internal

# MCP Server Configuration
MCP_SERVER_PORT=5002
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_BASE_URL=https://localhost
MCP_SERVER_INTERNAL_BASE_URL=https://host.docker.internal
MCP_SERVER_PATH=/mcp
MCP_SERVER_LOG_LEVEL=info
MCP_TRANSPORT_PROTOCOL=streamable-http
MCP_DEV_MODE=true

# IBKR MCP (used by multiple agents)
IBKR_MCP_URL=http://localhost:5002/mcp

# Google Cloud Platform (REQUIRED)
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

#### 2. Lancer les services

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier l'état des services
docker ps

# Voir les logs
docker-compose logs -f
```

#### 3. Authentification IBKR

**Important** : Le Gateway IBKR nécessite une authentification manuelle la première fois :

1. Ouvrez votre navigateur : `https://localhost:5055`
2. Acceptez le certificat auto-signé (Avancé → Accepter le risque)
3. Connectez-vous avec vos identifiants IBKR
4. Une fois connecté, le Gateway reste authentifié (session persistée)

Le **tickler** (script en arrière-plan) rafraîchit automatiquement la session toutes les 60 secondes pour éviter l'expiration.

#### 4. Tester la connexion

```bash
# Tester le Gateway IBKR
curl -k https://localhost:5055/v1/api/iserver/auth/status

# Tester le MCP Server
curl http://localhost:5002/mcp

# Tester l'application
curl http://localhost:8080/health
```

### Arrêter les services

```bash
# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

## Utilisation de l'interface ADK Web

### Lancer l'interface web ADK

L'application expose automatiquement l'interface ADK Web pour interagir avec les agents:

```bash
# Depuis le répertoire racine
adk web app/components/agents

# Ou via Docker Compose (déjà configuré)
docker-compose up -d

# Accéder à l'interface
# http://localhost:8080 (ou le port configuré dans .env)
```

**Agents disponibles dans l'interface ADK:**
- `portefolio_master_agent` - Orchestrateur du workflow autonome (5 sous-agents)
- `agent_with_vertex_rag` - Agent avec RAG Vertex AI

**Note importante:** Les sous-agents (`ibkr_reader_agent`, `market_reader_agent`, etc.) ne sont **pas** accessibles directement via l'interface ADK. Ils sont automatiquement exécutés dans l'ordre par `portefolio_master_agent`.

### Troubleshooting

#### Erreur "No root_agent found for 'X'"

Si vous voyez cette erreur, cela signifie qu'ADK ne trouve pas l'agent demandé.

**Cause la plus fréquente:** Vous essayez d'accéder à un sous-agent directement (exemple: `ibkr_reader_agent`, `market_reader_agent`, `decision_maker_agent`, etc.). Ces agents ne sont **pas** accessibles directement car ils n'exportent pas de `root_agent`.

**Solution:**
1. Utilisez `portefolio_master_agent` comme `app_name` dans vos requêtes API
2. Les sous-agents seront automatiquement exécutés dans l'ordre par l'orchestrateur
3. Pour accéder aux routes ADK (`/run`, `/run/sse`), utilisez:
   ```bash
   curl -X POST http://localhost:8080/run \
     -H "Content-Type: application/json" \
     -d '{
       "app_name": "portefolio_master_agent",
       "user_id": "user123",
       "session_id": "session456",
       "new_message": {
         "role": "user",
         "parts": [{"text": "Votre message ici"}]
       }
     }'
   ```

**Agents valides (exportent root_agent):**
- `portefolio_master_agent` - Orchestrateur principal du workflow
- `agent_with_vertex_rag` - Agent avec RAG Vertex AI

**Sous-agents (NON accessibles directement):**
- `ibkr_reader_agent`, `market_reader_agent`, `portfolio_evaluator_agent`, `decision_maker_agent`, `order_executor_agent`
- Ces agents sont appelés automatiquement par `portefolio_master_agent`

#### Le Gateway IBKR ne démarre pas

```bash
# Voir les logs du Gateway
docker logs api_gateway

# Vérifier le healthcheck
docker inspect api_gateway | grep Health -A 20
```

#### Le MCP Server ne peut pas se connecter au Gateway

```bash
# Vérifier la configuration réseau
docker network inspect portefolio-manager-adk_mcp_net

# Tester la connexion depuis le MCP Server
docker exec mcp_server curl -k https://host.docker.internal:5055/v1/api/iserver/auth/status
```

#### Les agents ne reçoivent pas de données

1. Vérifiez que vous êtes authentifié sur le Gateway IBKR
2. Consultez les logs du MCP Server : `docker logs mcp_server`
3. Vérifiez les variables d'environnement dans `.env`

## Stack 

- **Backend** : FastAPI
- **Framework Agent** : Google Agent Development Kit (ADK)
- **Cloud** : Google Cloud Platform (Cloud Run, Cloud Build, Artifact Registry)
- **Broker** : Interactive Brokers (IBKR)
- **Base de données** : Cloud SQL (gestion de sessions)

## Initialisation

### Mode Production (Docker Compose - Recommandé)

```bash
# 1. Configurer les variables d'environnement
cp .env.example .env
# Éditez .env avec vos identifiants GCP et autres configurations

# 2. Démarrer tous les services
docker-compose up -d

# 3. Se connecter au Gateway IBKR
# Ouvrez https://localhost:5055 dans votre navigateur
# Connectez-vous avec vos identifiants IBKR

# 4. Vérifier que tout fonctionne
docker ps
curl http://localhost:8080/health
```

### Mode Développement (Local)

Si vous souhaitez développer sans Docker :

```bash
# 1. Installer les dépendances
uv sync

# 2. Démarrer le Gateway IBKR (dans un terminal séparé)
cd ibkr
./bin/run.sh ./root/conf.yaml

# 3. Démarrer le MCP Server (dans un autre terminal)
cd mcp_server
uv run -- python fastapi_server.py

# 4. Démarrer l'application (dans un autre terminal)
uv run uvicorn app.main:app --reload --port 8080
```

**Note** : En mode développement, vous devez ajuster les URLs dans `.env` :
```bash
GATEWAY_INTERNAL_BASE_URL=https://localhost  # au lieu de https://host.docker.internal
IBKR_MCP_URL=http://localhost:5002/mcp
```

### Outils des Agents

**Agent Portefeuille Actions** (`stock_portfolio_agent`)

- `get_portfolio_accounts_portfolio_accounts_get`
- `get_account_summary_portfolio`
- `get_positions_portfolio`
- `get_position_by_conid_portfolio`
- `get_all_positions_by_conid_portfolio_positions`
- `get_combo_positions_portfolio`
- `get_account_ledger_portfolio`
- `get_account_allocation_portfolio`
- `get_all_accounts_allocation_portfolio_allocation_post`
- `get_account_meta_portfolio`
- `get_portfolio_subaccounts_portfolio_subaccounts_get`
- `get_portfolio_subaccounts_large_portfolio_subaccounts2_g`
- `invalidate_portfolio_cache_portfolio`
- `get_marketdata_snapshot_iserver_marketdata_snapshot_get`
- `get_md_snapshot_md_snapshot_get`
- `get_marketdata_history_iserver_marketdata_history_get`
- `get_hmds_history_hmds_history_get`
- `get_available_fields_iserver_marketdata_fields_get`
- `get_availability_codes_iserver_marketdata_availability_g`
- `get_iserver_history_rules_iserver_marketdata_history_rul`
- `get_hmds_history_rules_hmds_history_rules_get`
- `unsubscribe_market_data_iserver_marketdata_unsubscribe_p`
- `unsubscribe_all_market_data_iserver_marketdata_unsubscri`
- `get_marketdata_snapshot_iserver_marketdata_snapshot_get`
- `get_md_snapshot_md_snapshot_get`
- `get_marketdata_history_iserver_marketdata_history_get`
- `get_hmds_history_hmds_history_get`
- `get_available_fields_iserver_marketdata_fields_get`
- `get_availability_codes_iserver_marketdata_availability_g`
- `get_iserver_history_rules_iserver_marketdata_history_rul`
- `get_hmds_history_rules_hmds_history_rules_get`
- `unsubscribe_market_data_iserver_marketdata_unsubscribe_p`
- `unsubscribe_all_market_data_iserver_marketdata_unsubscri`
- `get_scanner_params_iserver_scanner_params_get`
- `run_scanner_iserver_scanner_run_post`
- `run_hmds_scanner_hmds_scanner_post`
- `search_contract_by_symbol_or_name_iserver_secdef_search_`
- `get_contract_info_iserver_contract`
- `get_contract_info_and_rules_iserver_contract`
- `get_secdef_info_iserver_secdef_info_get`
- `get_contract_rules_iserver_contract_rules_post`
- `get_contract_algos_iserver_contract`
- `get_strikes_iserver_secdef_strikes_get`
- `search_currency_pairs_iserver_secdef_currency_get`
- `get_bond_filters_iserver_secdef_bond_filters_get`
- `get_trsrv_futures_by_symbol_trsrv_futures_get`
- `get_stocks_by_symbol_trsrv_stocks_get`
- `get_secdef_by_conids_trsrv_secdef_get`
- `get_trading_schedule_trsrv_secdef_schedule_get`
- `get_events_contracts_events_contracts_get`
- `show_event_contract_events_show_get`

## Structure du Projet

```
portfolio-manager/
├── app/                      # Application principale FastAPI + ADK
│   ├── main.py               # Point d'entrée FastAPI
│   ├── components/           # Composants
│   │   ├── agents/           # Agents spécialisés
│   │   │   ├── market_reader_agent/        # Lecture données marché
│   │   │   ├── order_executor_agent/       # Exécution ordres
│   │   │   └── agent_with_vertex_rag/      # Agent avec RAG
│   │   └── callbacks/        # Callbacks de logging
│   ├── config/               # Configuration et settings
│   └── instructions/         # Templates d'instructions agents
│
├── api_gateway/              # Gateway IBKR Client Portal (Docker)
│   ├── Dockerfile            # Image Docker pour le Gateway
│   ├── conf.yaml             # Configuration du Gateway (port 5055)
│   ├── run_gateway.sh        # Script de démarrage
│   ├── healthcheck.sh        # Script de healthcheck
│   └── tickler.sh            # Script de maintien de session
│
├── mcp_server/               # Serveur MCP FastMCP (Docker)
│   ├── Dockerfile            # Image Docker pour le MCP Server
│   ├── fastapi_server.py     # Serveur FastMCP sur port 5002
│   ├── config.py             # Configuration (ports, URLs, tags)
│   ├── routers/              # Routes MCP par catégorie
│   │   ├── market_data.py    # Endpoints données marché
│   │   ├── portfolio.py      # Endpoints portfolio
│   │   ├── orders.py         # Endpoints ordres
│   │   └── session.py        # Endpoints session/auth
│   └── pyproject.toml        # Dépendances MCP Server
│
├── investment_policy/        # Politiques d'investissement
│   └── default_policy.yaml   # Policy par défaut (risque, allocation)
│
├── .cloudbuild/              # Pipeline CI/CD (Cloud Build)
├── deployment/               # Infrastructure Terraform
├── docker-compose.yml        # Orchestration des services
├── .env.example              # Template variables d'environnement
└── pyproject.toml            # Configuration et dépendances app
```

## Commandes Principales

### Docker (Production)

| Commande | Description |
|----------|-------------|
| `docker-compose up -d` | Démarre tous les services en arrière-plan |
| `docker-compose down` | Arrête tous les services |
| `docker-compose logs -f` | Affiche les logs en temps réel |
| `docker-compose ps` | Liste l'état des services |
| `docker-compose restart <service>` | Redémarre un service spécifique |
| `docker-compose build` | Reconstruit les images Docker |

### Développement Local

| Commande | Description |
|----------|-------------|
| `make install` | Installe les dépendances |
| `make playground` | Lance l'interface de développement |
| `make local-backend` | Serveur FastAPI avec hot-reload |
| `make test` | Exécute les tests |
| `make lint` | Vérifications de code |

### Déploiement Cloud

| Commande | Description |
|----------|-------------|
| `make deploy` | Déploie sur Cloud Run |
| `make setup-dev-env` | Configure l'infrastructure Terraform |


## Infrastructure GCP

```
GitHub → Cloud Build → Artifact Registry → Cloud Run
```

**Services déployés :**
- **Cloud Run** : API FastAPI multi-agents
- **Cloud Run** : MCP Server IBKR
- **Cloud SQL** : Gestion des sessions
- **Cloud Trace** : Télémétrie et monitoring
- **BigQuery** : Journalisation des requêtes LLM

### Variables d'Environnement

Créer un fichier `.env` à la racine :

```bash
PROJECT_ID=your-project-id
REGION=us-central1

IBKR_GATEWAY_URL=https://your-ibkr-gateway.run.app
IBKR_ACCOUNT_ID=your-account-id

MODEL_NAME=gemini-2.0-flash-exp
```

### Investment Policy

La policy d'investissement est configurée dans `investment_policy/default_policy.yaml` :

**Personnalisation** : Modifiez `default_policy.yaml` pour ajuster :
- Votre profil de risque (conservative/moderate/aggressive)
- Seuils de stop loss et take profit
- Allocation d'actifs cible
- Stratégies de trading activées
- Secteurs préférés et pondérations

**Télémétrie (toujours active)**
- **Cloud Trace** : Traces OpenTelemetry des agents
- **Cloud Logging** : Logs applicatifs
- **BigQuery** : Métriques LLM (jetons, latence, modèle)

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commit (`git commit -m 'Ajout fonctionnalité'`)
4. Push (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une Pull Request

## Ressources sympa

- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) - Template de base (v0.21.1)
- [Google ADK](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-builder) - Documentation officielle
- [IBKR API](https://www.interactivebrokers.com/api/) - Documentation Interactive Brokers

---

**Note** : Ce projet est basé sur l'Agent Starter Pack de Google Cloud Platform et démontre l'utilisation du Kit de Développement d'Agents (ADK) pour créer une solution d'analyse patrimoniale automatisée.