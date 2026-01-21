# Guide des règles Git à toujours respecter

Ce guide présente les bonnes pratiques Git à appliquer systématiquement dans un projet, que ce soit en équipe ou en solo.

---

## 1. Règles générales

* Ne jamais travailler directement sur la branche `main` ou `master`
* Chaque modification doit être liée à une branche dédiée
* Les commits doivent être clairs, petits et fréquents
* Toujours tirer les dernières modifications avant de commencer à travailler
* Ne jamais casser le build ou les tests existants

---

## 2. Création d’une branche

Lors de toute modification (feature, bug, refactor, doc), **créer une nouvelle branche**.

### Convention de nommage

* `feature/nom-feature`
* `fix/nom-bug`
* `refactor/nom-refactor`
* `docs/nom-doc`

### Exemple

```bash
git checkout -b feature/ajout-authentification
```

---

## 3. Avant de commencer à coder

* Se placer sur `main`
* Mettre à jour la branche locale

```bash
git checkout main
git pull origin main
```

* Créer ensuite la nouvelle branche

---

## 4. Règles de commit

### Bonnes pratiques

* Un commit = une action logique
* Éviter les commits trop gros
* Tester le code avant de commit

### Message de commit

Format recommandé :

```
<type>: description courte
```

Types courants :

* `feat`: nouvelle fonctionnalité
* `fix`: correction de bug
* `refactor`: refactorisation sans changement fonctionnel
* `docs`: documentation
* `test`: ajout/modification de tests
* `chore`: tâches techniques

### Exemple

```bash
git commit -m "feat: ajout du système de login"
```

---

## 5. Synchronisation avec la branche principale

Avant de pousser ou créer une Pull Request :

```bash
git checkout main
git pull origin main
git checkout feature/ajout-authentification
git merge main
```

* Résoudre les conflits proprement
* Tester après la fusion

---

## 6. Push de la branche

```bash
git push origin feature/ajout-authentification
```

* Ne jamais forcer un push (`--force`) sans raison valable

---

## 7. Pull Request (PR)

* Toujours passer par une Pull Request
* Décrire clairement :

  * Ce qui a été fait
  * Pourquoi
  * Comment tester

Checklist avant PR :

* [ ] Le code compile
* [ ] Les tests passent
* [ ] Le code est lisible
* [ ] Pas de fichiers inutiles

---

## 8. Après la validation

* Merger la PR sur `main`
* Supprimer la branche distante
* Mettre à jour la branche locale

```bash
git checkout main
git pull origin main
git branch -d feature/ajout-authentification
```

---

## 9. Règles à ne jamais enfreindre

* ❌ Commit directement sur `main`
* ❌ Pousser du code cassé
* ❌ Laisser des conflits non résolus
* ❌ Commits sans message clair
* ❌ Mélanger plusieurs sujets dans un commit

---

## 10. Raccourci mental à retenir

> **1 changement = 1 branche = plusieurs petits commits = 1 PR propre**

---

Si tu veux, je peux aussi te faire :

* une version ultra-courte (checklist)
* un guide GitFlow
* un template de message de commit
* un template de Pull Request
