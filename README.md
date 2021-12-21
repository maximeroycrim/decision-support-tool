# Decision Support Tool


1. install pre-commit

    pip install pre-commit
    pre-commit install

2. commit changes

    git commit -m "changed something in the notebook"
    (runs pre-commit checks)

3. tag version

    git tag <tag_name>
    git push origin <tag_name>
    (triggers a GitHub Action which builds and push Docker image)
