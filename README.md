# porte-folio-manager

Ce projet permet de montrer la puissance du Kit de Développement d'Agents (ADK) de Google et de fournir une base avec plusieurs modèles. 

A travers ce projet je souhaite créer un solution agentic pour faire de l'analyse de patrimoine et 
automatiser l'investissement. Pour cela je vais utiliser IBKR (cf. Interactivebrokers) un broker
qui permet d'acheter et vendre des produits financiers. 

Je vais mettre en place le protocol MCP pour IBKR.

L'agent porte-folio-manager dispose de trois sous agents :

├-── porte-folio-manager              
    ├── Agent spécialiste en immobilier
    ├── Agent spécialiste de l'analyse de porte feuille d'actions
    └── Agent spécialiste des marchés 

Les outils des différents agents :

├-── Agent spécialiste de l'analyse de porte feuille d'actions (stock_portfolio_agent)
    ├── Portefeuille et Compte :
        - get_portfolio_accounts_portfolio_accounts_get
        - get_account_summary_portfolio
        - get_positions_portfolio
        - get_position_by_conid_portfolio
        - get_all_positions_by_conid_portfolio_positions
        - get_combo_positions_portfolio
        - get_account_ledger_portfolio
        - get_account_allocation_portfolio
        - get_all_accounts_allocation_portfolio_allocation_post
        - get_account_meta_portfolio
        - get_portfolio_subaccounts_portfolio_subaccounts_get
        - get_portfolio_subaccounts_large_portfolio_subaccounts2_g
        - invalidate_portfolio_cache_portfolio
    └── Données de Marché :
        - get_marketdata_snapshot_iserver_marketdata_snapshot_get
        - get_md_snapshot_md_snapshot_get
        - get_marketdata_history_iserver_marketdata_history_get
        - get_hmds_history_hmds_history_get
        - get_available_fields_iserver_marketdata_fields_get
        - get_availability_codes_iserver_marketdata_availability_g
        - get_iserver_history_rules_iserver_marketdata_history_rul
        - get_hmds_history_rules_hmds_history_rules_get
        - unsubscribe_market_data_iserver_marketdata_unsubscribe_p
        - unsubscribe_all_market_data_iserver_marketdata_unsubscri

├-── Agent spécialiste des marchés (market_specialist_agent)
    ├── Données de Marché :
        - get_marketdata_snapshot_iserver_marketdata_snapshot_get
        - get_md_snapshot_md_snapshot_get
        - get_marketdata_history_iserver_marketdata_history_get
        - get_hmds_history_hmds_history_get
        - get_available_fields_iserver_marketdata_fields_get
        - get_availability_codes_iserver_marketdata_availability_g
        - get_iserver_history_rules_iserver_marketdata_history_rul
        - get_hmds_history_rules_hmds_history_rules_get
        - unsubscribe_market_data_iserver_marketdata_unsubscribe_p
        - unsubscribe_all_market_data_iserver_marketdata_unsubscri
    ├── Scanners de Marché :
        - get_scanner_params_iserver_scanner_params_get
        - run_scanner_iserver_scanner_run_post
        - run_hmds_scanner_hmds_scanner_post
    └── Contrats et Recherche (SecDef) :
        - search_contract_by_symbol_or_name_iserver_secdef_search_
        - get_contract_info_iserver_contract
        - get_contract_info_and_rules_iserver_contract
        - get_secdef_info_iserver_secdef_info_get
        - get_contract_rules_iserver_contract_rules_post
        - get_contract_algos_iserver_contract
        - get_strikes_iserver_secdef_strikes_get
        - search_currency_pairs_iserver_secdef_currency_get
        - get_bond_filters_iserver_secdef_bond_filters_get
        - get_trsrv_futures_by_symbol_trsrv_futures_get
        - get_stocks_by_symbol_trsrv_stocks_get
        - get_secdef_by_conids_trsrv_secdef_get
        - get_trading_schedule_trsrv_secdef_schedule_get
        - get_events_contracts_events_contracts_get
        - show_event_contract_events_show_get

├-── Agent spécialiste en immobilier (real_estate_specialist_agent)
    └── Aucun outil IBKR (spécialisé en immobilier via BigQuery)

---

Le modèle pour big query : 

Pour les transactions je veux le type de compte PEA, CTO, Assurance vie
Je veux pouvoir renseigner mes transactions achat/vente avec le code ISN, date d'achat, prix unitaire, frais payé pour la transaction, le nom de l'action ou produit financier
Je veux une table qui puisse suivre ma plu-value latente lorsque le le demande il calcul et insert la donnée dans la table.

Par exemple : 
Trade Republic : PEA, CTO
Bourso banque : Compte courant, PEA, Assurance vie, Compte entreprise

---
CREATE TABLE lil-onboard-gcp.portefolio_manager.comptes (
compte_id STRING NOT NULL OPTIONS(description="Identifiant unique pour chaque compte (ex: UUID)"),
user_id STRING NOT NULL OPTIONS(description="Identifiant de l'utilisateur propriétaire du compte"),
nom_compte STRING OPTIONS(description="Nom personnalisé du compte (ex: 'PEA Boursorama')"),
type_compte STRING NOT NULL OPTIONS(description="Type de compte (ex: 'PEA', 'CTO', 'Assurance Vie', 'Compte Courant')"),
courtier STRING NOT NULL OPTIONS(description="Nom de l'établissement financier (ex: 'Trade Republic', 'Boursorama')"),
date_creation TIMESTAMP OPTIONS(description="Date d'ouverture du compte"),
devise STRING NOT NULL OPTIONS(description="Devise principal du compte (ex: 'EUR', 'USD')")
);
---
CREATE TABLE lil-onboard-gcp.portefolio_manager.transactions (
 transaction_id STRING NOT NULL OPTIONS(description="Identifiant unique pour chaque transaction"),
compte_id STRING NOT NULL OPTIONS(description="Clé étrangèr qui référence la table 'comptes'"),
user_id STRING NOT NULL OPTIONS(description="Identifiant de l'utilisateur pour la transaction"),
isin STRING NOT NULL OPTIONS(description="Code ISIN du produit financier"),
nom_produit STRING OPTIONS(description="Nom de l'action ou produit financier"),
type_transaction STRING NOT NULL OPTIONS(description="Type d'opération : 'ACHAT' ou 'VENTE'"),
date_transaction TIMESTAMP NOT NULL OPTIONS(description="Date et heure de la transaction"),
quantite FLOAT64 NOT NULL OPTIONS(description="Nombre d'unités achetées ou vendues"),
prix_unitaire FLOAT64 NOT NULL OPTIONS(description="Prix d'une seule unité au moment de la transaction"),
frais_transaction FLOAT64 OPTIONS(description="Frais payés pour cette transaction"),
devise STRING NOT NULL OPTIONS(description="Devise de la transaction"));
---
CREATE TABLE lil-onboard-gcp.portefolio_manager.plus_values_latentes (
snapshot_id STRING NOT NULL OPTIONS(description="Identifiant unique pour cet instantané de calcul"),
user_id STRING NOT NULL OPTIONS(description="Identifiant de l'utilisateur"),
compte_id STRING NOT NULL OPTIONS(description="Identifiant compte concerné"),
isin STRING NOT NULL OPTIONS(description="Code ISIN de l'actif"),
quantite_actuelle FLOAT64 OPTIONS(description="Quantité totale détenue au moment du calcul"),
pru FLOAT64 OPTIONS(description="Prix de Revient Unitaire moyen, incluant les frais"),
cours_actuel FLOAT64 OPTIONS(description="Cours du marché a moment du calcul"),
plus_value_latente FLOAT64 OPTIONS(description="Montant de plus-value ou moins-value latente (Quantité * (Cours actuel - PRU))"),
date_snapshot TIMESTAMP NOT NULL OPTIONS(description="Date heure du calcul")
);
---

Un agent ReAct de base construit avec le Kit de Développement d'Agents (ADK) de Google.
Agent généré avec [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.21.1`

## Structure du Projet

Ce projet est organisé comme suit :

```
porte-folio-manager/
├── app/                 # Code de l'application principale
│   ├── agent.py         # Logique principale de l'agent
│   ├── fast_api_app.py  # Serveur FastAPI Backend
│   └── app_utils/       # Utilitaires et assistants de l'application
├── .cloudbuild/         # Configurations de pipeline CI/CD pour Google Cloud Build
├── deployment/          # Scripts d'infrastructure et de déploiement
├── notebooks/           # Notebooks Jupyter pour le prototypage et l'évaluation
├── tests/               # Tests unitaires, d'intégration et de charge
├── Makefile             # Makefile pour les commandes courantes
├── GEMINI.md            # Guide de développement assisté par l'IA
└── pyproject.toml       # Dépendances et configuration du projet
```

## Prérequis

Avant de commencer, assurez-vous d'avoir :
- **uv**: Gestionnaire de paquets Python (utilisé pour toute la gestion des dépendances dans ce projet) - [Installer](https://docs.astral.sh/uv/getting-started/installation/) ([ajouter des paquets](https://docs.astral.sh/uv/concepts/dependencies/) avec `uv add <package>`)
- **Google Cloud SDK**: Pour les services GCP - [Installer](https://cloud.google.com/sdk/docs/install)
- **Terraform**: Pour le déploiement de l'infrastructure - [Installer](https://developer.hashicorp.com/terraform/downloads)
- **make**: Outil d'automatisation de la construction - [Installer](https://www.gnu.org/software/make/) (pré-installé sur la plupart des systèmes Unix)


## Démarrage Rapide (Tests Locaux)

Installez les paquets requis et lancez l'environnement de développement local :

```bash
make install && make playground
```
> **📊 Note d'Observabilité :** La télémétrie de l'agent (Cloud Trace) est toujours activée. La journalisation des requêtes-réponses (GCS, BigQuery, Cloud Logging) est **désactivée** localement, **activée par défaut** dans les environnements déployés (métadonnées uniquement - pas de requêtes/réponses). Voir [Surveillance et Observabilité](#surveillance-et-observabilite) pour plus de détails.

## Commandes

| Commande             | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make install`       | Installe toutes les dépendances requises à l'aide de uv                                     |
| `make playground`    | Lance l'environnement de développement local avec le backend et le frontend - utilisant la commande `adk web`.|
| `make deploy`        | Déploie l'agent sur Cloud Run (utilisez `IAP=true` pour activer Identity-Aware Proxy, `PORT=8080` pour spécifier le port du conteneur) |
| `make local-backend` | Lance le serveur de développement local avec rechargement à chaud                             |
| `make test`          | Exécute les tests unitaires et d'intégration                                                |
| `make lint`          | Exécute les vérifications de qualité de code (codespell, ruff, mypy)                       |
| `make setup-dev-env` | Configure les ressources de l'environnement de développement à l'aide de Terraform         |

Pour toutes les options de commande et l'utilisation, veuillez vous référer au [Makefile](Makefile).


## Utilisation

Ce modèle suit une approche "apportez votre propre agent" - vous vous concentrez sur votre logique métier, et le modèle gère tout le reste (interface utilisateur, infrastructure, déploiement, surveillance).

1.  **Prototypage :** Construisez votre agent d'IA générative en vous aidant des notebooks d'introduction dans `notebooks/`. Utilisez Vertex AI Evaluation pour évaluer les performances.
2.  **Intégration :** Importez votre agent dans l'application en éditant `app/agent.py`.
3.  **Test :** Explorez les fonctionnalités de votre agent à l'aide du playground local avec `make playground`. Le playground recharge automatiquement votre agent lors des modifications de code.
4.  **Déploiement :** Configurez et lancez les pipelines CI/CD, en personnalisant les tests si nécessaire. Référez-vous à la section [déploiement](#déploiement) pour des instructions complètes. Pour un déploiement d'infrastructure simplifié, exécutez simplement `uvx agent-starter-pack setup-cicd`. Consultez la commande CLI [`agent-starter-pack setup-cicd`](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html). Prend actuellement en charge GitHub avec Google Cloud Build et GitHub Actions comme exécuteurs CI/CD.
5.  **Surveillance :** Suivez les performances et recueillez des informations à l'aide des données de télémétrie BigQuery, de Cloud Logging et de Cloud Trace pour itérer sur votre application.

Le projet inclut un fichier `GEMINI.md` qui fournit le contexte aux outils d'IA comme Gemini CLI lorsque vous posez des questions sur votre modèle.


## Déploiement

> **Note :** Pour un déploiement simplifié en une seule commande de l'ensemble du pipeline CI/CD et de l'infrastructure à l'aide de Terraform, vous pouvez utiliser la commande CLI [`agent-starter-pack setup-cicd`](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html). Prend actuellement en charge GitHub avec Google Cloud Build et GitHub Actions comme exécuteurs CI/CD.

### Environnement de Développement

Vous pouvez tester le déploiement vers un environnement de développement en utilisant la commande suivante :

```bash
gcloud config set project <your-dev-project-id>
make deploy
```


Le dépôt inclut une configuration Terraform pour la configuration du projet Google Cloud de développement.
Voir [deployment/README.md](deployment/README.md) pour les instructions.

### Déploiement en Production

Le dépôt inclut une configuration Terraform pour la configuration d'un projet Google Cloud de production. Référez-vous à [deployment/README.md](deployment/README.md) pour des instructions détaillées sur la façon de déployer l'infrastructure et l'application.

## Surveillance et Observabilité

L'application offre deux niveaux d'observabilité :

**1. Événements de télémétrie de l'agent (toujours activés)**
- Traces et spans OpenTelemetry exportées vers **Cloud Trace**
- Suivi de l'exécution de l'agent, de la latence et des métriques système

**2. Journalisation des requêtes-réponses (configurable)**
- L'instrumentation GenAI capture les interactions LLM (jetons, modèle, timing)
- Exporté vers **Google Cloud Storage** (JSONL), **BigQuery** (tables externes) et **Cloud Logging** (bucket dédié)

| Environnement | Journalisation des requêtes-réponses |
|-------------|-------------------------|
| **Développement Local** (`make playground`) | ❌ Désactivé par défaut |
| **Environnements Déployés** (via Terraform) | ✅ **Activé par défaut** (respectueux de la vie privée : métadonnées uniquement, pas de requêtes/réponses) |

**Pour activer localement :** Définissez `LOGS_BUCKET_NAME` et `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`.

**Pour désactiver dans les déploiements :** Modifiez la configuration Terraform pour définir `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=false`.

Consultez le [guide d'observabilité](https://googlecloudplatform.github.io/agent-starter-pack/guide/observability.html) pour des instructions détaillées, des exemples de requêtes et des options de visualisation.
