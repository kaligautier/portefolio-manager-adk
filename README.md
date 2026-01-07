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
curl -X POST https://your-app.run.app/run/daily
```

### Option 3: APScheduler (Local)


Pour tester en local, ajoutez dans `application.py` :

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(trigger_daily, 'cron', hour=10, minute=0, day_of_week='mon-fri')
scheduler.start()
```

## Objectifs

Créer une solution agentique pour l'analyse de patrimoine et l'automatisation de l'investissement en utilisant :
- **IBKR** (Interactive Brokers) : courtier pour l'achat/vente de produits financiers
- **Protocole MCP** : intégration avec IBKR
- **ADK Google** : Kit de Développement d'Agents

## Mise en garde 

Le MCP IBKR demande une api gateway ou il faut se connecter avec son login/passwd depuis le navigateur. 

Pour lancer l'api gateway à la main : 

`clientportal.gw % ./bin/run.sh ./root/conf.yaml``

Il y a la possibilité de lancer api gateway dans un container avec un mécanisme de raffraichissement pour éviter de se connecter à nouveau.

## Stack 

- **Backend** : FastAPI
- **Framework Agent** : Google Agent Development Kit (ADK)
- **Cloud** : Google Cloud Platform (Cloud Run, Cloud Build, Artifact Registry)
- **Broker** : Interactive Brokers (IBKR)
- **Base de données** : Cloud SQL (gestion de sessions)

## Initialisation 

```bash
uv sync

uv run uvicorn app.main:app --reload --port 8085

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
├── app/                 # Application principale
│   ├── agent.py         # Logique des agents
│   ├── fast_api_app.py  # API FastAPI
│   └── components/      # Agents spécialisés
├── .cloudbuild/         # Pipeline CI/CD (Cloud Build)
├── deployment/          # Infrastructure Terraform
├── api_gateway/         # Passerele pour le MCP IBKR
├── notebooks/           # Prototypage et évaluation
├── tests/               # Tests (unitaires, intégration)
└── pyproject.toml       # Configuration et dépendances
```

## Commandes Principales

| Commande | Description |
|----------|-------------|
| `make install` | Installe les dépendances |
| `make playground` | Lance l'interface de développement |
| `make local-backend` | Serveur FastAPI avec hot-reload |
| `make test` | Exécute les tests |
| `make lint` | Vérifications de code |
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