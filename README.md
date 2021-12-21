# Decision Support Tool


1. Install `pre-commit`

    ```
    pip install pre-commit
    pre-commit install
    ```

2. Commit changes

    ```
    git commit -m "changed something in the notebook"
    ```
    
    Runs `pre-commit` checks locally.

3. Edit `CHANGELOG.md` accordingly

4. Tag version

    ```
    git tag <tag_name>
    git push origin <tag_name>
    ```

    Triggers a GitHub Action which builds and push Docker image.
