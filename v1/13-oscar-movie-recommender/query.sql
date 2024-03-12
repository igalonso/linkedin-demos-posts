# first import the movie CSV into raw.

CREATE OR REPLACE MODEL oscar_winners.llm_model
  REMOTE WITH CONNECTION `us.llm_conn`
  OPTIONS (remote_service_type = 'CLOUD_AI_LARGE_LANGUAGE_MODEL_V1');


CREATE OR REPLACE TABLE `gen-ai-igngar.oscar_winners.refined` AS
SELECT
  raw.*,
  SPLIT(TRIM(JSON_VALUE((SAFE.PARSE_JSON(generated_text.json_response)["generated_text"]))), ',') AS Categories
FROM
  `gen-ai-igngar.oscar_winners.raw` AS raw
JOIN (
SELECT
   TO_JSON_STRING(
    STRUCT(
     ml_generate_text_result['predictions'][0]['content'] AS generated_text
    )
  ) AS json_response,
  Film
FROM
  ML.GENERATE_TEXT(MODEL `gen-ai-igngar.oscar_winners.llm_model`, (
    SELECT
      CONCAT("can you give me the genre of the following films using this example format: genre1,genre2 \nAll the genres of the film in lowercase'}: ", ARRAY_TO_STRING([Film], ",")) AS prompt,
      Film 
    FROM
      `gen-ai-igngar.oscar_winners.raw`
  ),
    STRUCT(
      0 AS temperature,
      100 AS max_output_tokens))
) AS generated_text
ON raw.Film = generated_text.Film;

CREATE OR REPLACE TABLE `gen-ai-igngar.oscar_winners.refined` AS
SELECT
  *,
  CASE
    WHEN Award > 0 THEN TRUE
    ELSE FALSE
  END AS Winner
FROM
  `gen-ai-igngar.oscar_winners.refined`;


SELECT DISTINCT category
FROM `gen-ai-igngar.oscar_winners.refined`,
UNNEST(Categories) AS category;

SELECT *
FROM `gen-ai-igngar.oscar_winners.refined`
WHERE winner = TRUE 
ORDER BY Year DESC;