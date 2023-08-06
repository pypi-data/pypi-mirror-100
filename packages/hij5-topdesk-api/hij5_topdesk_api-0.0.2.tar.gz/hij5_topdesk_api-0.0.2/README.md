## Hoe update je dit ding?

1. Pas de versie aan in setup.cfg
1. `python -m build`
1. `python -m twine upload dist/*`
1. Gebruik als username `__token__` en als password de API token.