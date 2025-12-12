# 🚀 Guide de Déploiement Rapide - Portfolio Manager

## Étape 1: Configuration IAM (À faire une seule fois) ⚙️

Exécutez ce script pour créer les service accounts et permissions nécessaires:

```bash
cd iac
./setup-iam.sh lil-onboard-gcp
```

**Ce que fait le script:**
- ✅ Crée le service account `porte-folio-manager-sa` pour l'application
- ✅ Accorde les permissions Vertex AI, Logging, Trace, Storage
- ✅ Accorde les permissions Cloud Build pour déployer

## Étape 2: Déployer via Cloud Build 🏗️

Une fois les permissions configurées, déployez simplement:

```bash
# Ajoutez tous les fichiers
git add .

# Commitez
git commit -m "feat: add Cloud Run deployment with IAM setup"

# Poussez vers GitHub
git push origin feat/add-cloudbuild
```

Cloud Build va automatiquement:
1. ✅ Créer l'Artifact Registry
2. ✅ Activer les APIs nécessaires
3. ✅ Builder l'image Docker
4. ✅ Déployer sur Cloud Run

## Étape 3: Vérifier le déploiement ✅

Une fois le build terminé:

1. **Récupérer l'URL du service:**
   ```bash
   gcloud run services describe porte-folio-manager \
     --region europe-west1 \
     --project lil-onboard-gcp \
     --format 'value(status.url)'
   ```

2. **Tester le service:**
   ```bash
   curl https://YOUR-CLOUD-RUN-URL/
   ```

## Troubleshooting 🔧

### Erreur: Permission denied sur Artifact Registry ou IAM

**Solution:** Relancez le script de setup IAM:
```bash
cd iac
./setup-iam.sh lil-onboard-gcp
```

### Erreur: Service account not found

**Solution:** Le service account n'existe pas encore. Créez-le manuellement:
```bash
gcloud iam service-accounts create porte-folio-manager-sa \
  --display-name="Portfolio Manager Service Account" \
  --project=lil-onboard-gcp
```

### Voir les logs de déploiement

```bash
# Via Cloud Console
https://console.cloud.google.com/cloud-build/builds

# Ou via CLI
gcloud builds list --project=lil-onboard-gcp --limit=5
```

## Architecture Déployée 🏛️

```
┌─────────────────────────────────────────┐
│         GitHub Repository                │
└──────────────┬──────────────────────────┘
               │ git push
               ▼
┌─────────────────────────────────────────┐
│         Cloud Build                      │
│  - Terraform (Infrastructure)            │
│  - Docker Build                          │
│  - Deploy to Cloud Run                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Artifact Registry                     │
│    (Docker images)                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Cloud Run                        │
│  - Service: porte-folio-manager          │
│  - Port: 8080                            │
│  - Scale: 0-10 instances                 │
│  - Public access                         │
└─────────────────────────────────────────┘
```

## Ressources Créées 📦

- **Artifact Registry**: `europe-west1-docker.pkg.dev/lil-onboard-gcp/porte-folio-manager-repo`
- **Cloud Run Service**: `porte-folio-manager`
- **Service Account**: `porte-folio-manager-sa@lil-onboard-gcp.iam.gserviceaccount.com`

## Prochaines Étapes 🎯

1. Configurez un domaine personnalisé (optionnel)
2. Ajoutez l'authentification si nécessaire
3. Configurez les variables d'environnement supplémentaires
4. Mettez en place le monitoring et les alertes
