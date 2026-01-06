# Documentation de référence : API Interactive Brokers

Ce document répertorie les fonctions disponibles classées par domaine fonctionnel.

## Table des matières

1. [Authentification et Session](#authentification-et-session)
2. [Portefeuille et Compte](#portefeuille-et-compte)
3. [Ordres et Transactions](#ordres-et-transactions)
4. [Données de Marché](#données-de-marché)
5. [Contrats et Recherche (SecDef)](#contrats-et-recherche-secdef)
6. [Scanners de Marché](#scanners-de-marché)
7. [Gestion des Alertes](#gestion-des-alertes)
8. [Listes de Surveillance (Watchlists)](#listes-de-surveillance-watchlists)
9. [Notifications (FYI)](#notifications-fyi)



## Authentification et Session

Fonctions relatives à la validation SSO, au statut de l'authentification et au maintien de la session active.

| Fonction | Description |
| :--- | :--- |
| `sso_validate_sso_validate_post` | Valide la session SSO actuelle. |
| `get_auth_status_iserver_auth_status_get` | Récupère le statut d'authentification iServer. |
| `reauthenticate_iserver_reauthenticate_post` | Réauthentifie la session pour iServer. |
| `tickle_tickle_get` | Maintient la session active (heartbeat). |
| `logout_logout_post` | Déconnecte l'utilisateur et ferme la session. |



## Portefeuille et Compte

Fonctions permettant de récupérer les soldes, les positions, les allocations d'actifs et les métadonnées des comptes.

| Fonction | Description |
| :--- | :--- |
| `get_portfolio_accounts_portfolio_accounts_get` | Récupère la liste des comptes de portefeuille. |
| `get_account_summary_portfolio` | Récupère le résumé financier du compte de portefeuille. |
| `get_positions_portfolio` | Récupère les positions actuelles du portefeuille. |
| `get_position_by_conid_portfolio` | Récupère une position spécifique par son identifiant de contrat (conid). |
| `get_all_positions_by_conid_portfolio_positions` | Récupère toutes les positions associées à un conid. |
| `get_combo_positions_portfolio` | Récupère les positions combinées (stratégies complexes). |
| `get_account_ledger_portfolio` | Récupère le grand livre (ledger) du compte. |
| `get_account_allocation_portfolio` | Récupère l'allocation d'actifs du compte. |
| `get_all_accounts_allocation_portfolio_allocation_post` | Récupère l'allocation agrégée de tous les comptes. |
| `get_account_meta_portfolio` | Récupère les métadonnées du compte. |
| `get_portfolio_subaccounts_portfolio_subaccounts_get` | Liste les sous-comptes (pour structures Advisor/IBroker). |
| `get_portfolio_subaccounts_large_portfolio_subaccounts2_g` | Récupère les sous-comptes de portefeuille (liste étendue). |
| `invalidate_portfolio_cache_portfolio` | Invalide le cache du portefeuille pour forcer une mise à jour. |


## Ordres et Transactions

Fonctions de suivi des ordres en cours et d'accès à l'historique des transactions.

| Fonction | Description |
| :--- | :--- |
| `get_live_orders_iserver_account_orders_get` | Récupère les ordres actifs (en direct) pour le compte iServer. |
| `get_order_status_iserver_account_order_status` | Récupère le statut précis d'un ordre spécifique. |
| `get_trades_iserver_account_trades_get` | Récupère l'historique des transactions exécutées. |

---

## Données de Marché

Fonctions d'accès aux flux de prix, aux historiques et aux instantanés de marché.

| Fonction | Description |
| :--- | :--- |
| `get_marketdata_snapshot_iserver_marketdata_snapshot_get` | Récupère un instantané des données de marché iServer. |
| `get_md_snapshot_md_snapshot_get` | Récupère un instantané global des données de marché. |
| `get_marketdata_history_iserver_marketdata_history_get` | Récupère l'historique des données de marché via iServer. |
| `get_hmds_history_hmds_history_get` | Récupère l'historique via le service HMDS. |
| `get_available_fields_iserver_marketdata_fields_get` | Récupère la liste des champs de données disponibles. |
| `get_availability_codes_iserver_marketdata_availability_g` | Retourne le dictionnaire des codes de disponibilité des données. |
| `get_iserver_history_rules_iserver_marketdata_history_rul` | Récupère les règles de récupération d'historique (iServer). |
| `get_hmds_history_rules_hmds_history_rules_get` | Récupère les règles de récupération d'historique (HMDS). |
| `unsubscribe_market_data_iserver_marketdata_unsubscribe_p` | Se désabonne d'un flux de données spécifique. |
| `unsubscribe_all_market_data_iserver_marketdata_unsubscri` | Se désabonne de tous les flux de données de marché. |


## Contrats et Recherche (SecDef)

Fonctions de recherche d'instruments financiers et de récupération des définitions de sécurité.

| Fonction | Description |
| :--- | :--- |
| `search_contract_by_symbol_or_name_iserver_secdef_search_` | Recherche des contrats par symbole ou nom de société. |
| `get_contract_info_iserver_contract` | Récupère les informations détaillées d'un contrat. |
| `get_contract_info_and_rules_iserver_contract` | Récupère les informations d'un contrat ainsi que ses règles. |
| `get_secdef_info_iserver_secdef_info_get` | Récupère les informations de définition de sécurité. |
| `get_contract_rules_iserver_contract_rules_post` | Retourne les règles de trading pour un contrat donné. |
| `get_contract_algos_iserver_contract` | Retourne une liste d'algorithmes IB disponibles pour un contrat. |
| `get_strikes_iserver_secdef_strikes_get` | Obtient la liste des prix d'exercice (strikes) pour les options. |
| `search_currency_pairs_iserver_secdef_currency_get` | Recherche des paires de devises. |
| `get_bond_filters_iserver_secdef_bond_filters_get` | Retourne une liste de filtres d'obligations par émetteur. |
| `get_trsrv_futures_by_symbol_trsrv_futures_get` | Récupère les contrats futures par symbole via TRSV. |
| `get_stocks_by_symbol_trsrv_stocks_get` | Récupère les actions par symbole via TRSV. |
| `get_secdef_by_conids_trsrv_secdef_get` | Récupère les définitions de sécurité par conids via TRSV. |
| `get_trading_schedule_trsrv_secdef_schedule_get` | Récupère le calendrier des horaires de trading. |
| `get_events_contracts_events_contracts_get` | Récupère les événements liés aux contrats. |
| `show_event_contract_events_show_get` | Affiche le détail d'un événement pour un contrat. |


## Scanners de Marché

Outils pour filtrer et rechercher des opportunités sur le marché.

| Fonction | Description |
| :--- | :--- |
| `get_scanner_params_iserver_scanner_params_get` | Récupère les paramètres disponibles pour configurer un scan. |
| `run_scanner_iserver_scanner_run_post` | Exécute un scanner de marché iServer (top 100 résultats). |
| `run_hmds_scanner_hmds_scanner_post` | Exécute le scanner via le service HMDS. |

---

## Gestion des Alertes

Fonctions pour créer, modifier et gérer les alertes de prix et de compte.

| Fonction | Description |
| :--- | :--- |
| `create_or_modify_alert_iserver_account` | Crée ou modifie une alerte pour le compte iServer. |
| `activate_deactivate_alert_iserver_account_alert_activate` | Active ou désactive une alerte existante. |
| `delete_alert_iserver_account` | Supprime une alerte pour le compte iServer. |
| `get_mta_alert_iserver_account_mta_get` | Récupère les alertes MTA (Mobile Trading Assistant). |


## Listes de Surveillance (Watchlists)

Gestion des listes de suivi d'instruments.

| Fonction | Description |
| :--- | :--- |
| `get_watchlists_iserver_account_watchlists_get` | Récupère les watchlists existantes pour le compte. |
| `get_watchlist_contracts_iserver_account_watchlist` | Retourne la liste des contrats contenus dans une watchlist. |
| `create_watchlist_iserver_account` | Crée une nouvelle watchlist. |
| `delete_watchlist_iserver_account_watchlist` | Supprime une watchlist existante. |
| `add_contracts_to_watchlist_iserver_account_watchlist` | Ajoute des contrats à une watchlist spécifique. |
| `delete_contract_from_watchlist_iserver_account_watchlist` | Supprime un contrat d'une watchlist. |


## Notifications (FYI)

Gestion des messages système et des notifications informatives.

| Fonction | Description |
| :--- | :--- |
| `get_notifications_fyi_notifications_get` | Récupère la liste des notifications FYI. |
| `get_fyi_unread_number_fyi_unreadnumber_get` | Retourne le nombre total de notifications non lues. |
| `mark_notifications_as_read_fyi_notifications_delete` | Marque les notifications comme lues. |
| `get_fyi_settings_fyi_settings_post` | Retourne la liste des types de notifications (disclaimers). |
|