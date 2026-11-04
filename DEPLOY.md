# Deploy to Streamlit Community Cloud

1. Open [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Choose **New app**. If prompted, authorize access to the private repository `Mahmoud-Magdy67/product-marketing-analytics`.
3. Select the repository and its `main` branch. Set the main file path to `app.py`.
4. Confirm that `requirements.txt` is at the repository root. Community Cloud installs these dependencies automatically. The app reads committed `data/processed/*.parquet` files, so no secrets, database, or raw CSV download is needed.
5. Choose **Deploy** and wait for the app to finish building. Open each of the three tabs to check that the charts render.
6. Copy the resulting `.streamlit.app` URL into the live-demo link in `README.md` and, if desired, the GitHub repository description.

The repository is private. Share the deployed URL only with people who should see the portfolio app, and review Community Cloud's visibility setting during deployment.

`.streamlit/config.toml` sets a 200 MB limit for interactive file uploads. It does not change the size or loading behavior of the Parquet files bundled in the repository.
