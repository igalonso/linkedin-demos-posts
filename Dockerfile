FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:latest
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN python3 analytics-script.py

CMD ["streamlit", "run", "🏠_Home.py", "--server.port", "8095"]