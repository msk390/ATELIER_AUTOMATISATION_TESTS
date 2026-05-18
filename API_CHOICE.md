# API Choice

- Étudiant : OUAZIL Mimoun
- API choisie : Frankfurter
- URL base : https://api.frankfurter.app
- Documentation officielle : https://www.frankfurter.app/docs/
- Auth : None
- Endpoints testés :
  - GET /latest?from=EUR
  - GET /invalid_endpoint_xyz
- Hypothèses de contrat (champs attendus, types, codes) :
  - HTTP 200 attendu sur /latest
  - Content-Type: application/json
  - Champs présents : amount, base, date, rates
  - rates est un objet non vide
  - base == "EUR"
- Limites / rate limiting connu : aucune limite documentée
- Risques : downtime possible, données financières en temps réel
