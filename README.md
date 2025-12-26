## Portfolio Manager Multi-Agents

Gestionnaire de portefeuille multi-agents permettant de passer des ordres sur Interactive Brokers (IBKR), d'analyser son portefeuille, d'évaluer des actions et d'identifier les tendances de marché.

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

## Architecture Multi-Agents 

```
portfolio-manager (agent principal)
├── Agent Analyse d'Actions
└── Agent Marchés
    ├── Agent Presse Financière (en développement)
    ├── Agent Performance Historique (en développement)
    ├── Agent Macro-économie (en développement)
    └── Agent Régulation & Politique (en développement)
```

### Outils des Agents

**Agent Portefeuille Actions** (`stock_portfolio_agent`)

*Portefeuille et Compte :*
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

*Données de Marché :*
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

**Agent Marchés** (`market_specialist_agent`)

*Données de Marché :*
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

*Scanners de Marché :*
- `get_scanner_params_iserver_scanner_params_get`
- `run_scanner_iserver_scanner_run_post`
- `run_hmds_scanner_hmds_scanner_post`

*Contrats et Recherche (SecDef) :*
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

## Configuration

Créer un fichier `.env` à la racine :

```bash
PROJECT_ID=your-project-id
REGION=us-central1

IBKR_GATEWAY_URL=https://your-ibkr-gateway.run.app
IBKR_ACCOUNT_ID=your-account-id

MODEL_NAME=gemini-2.0-flash-exp
```

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