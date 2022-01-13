# Decision Support Tool


1. Install `pre-commit`

    ```
    pip install pre-commit
    pre-commit install
    ```

2. Edit `CHANGELOG.md` accordingly

3. Add changes to git staging env

    ```
    git add -A
    ```

3. Commit changes

    ```
    git commit -m "changed something in the notebook"
    ```
    
    Runs `pre-commit` checks locally.

4. Tag version

    ```
    git tag <tag_name>
    git push origin <tag_name>
    ```

    Triggers a GitHub Action which builds and push Docker image.
