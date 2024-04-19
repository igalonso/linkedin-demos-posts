CREATE OR REPLACE MODEL `conference_connect.embedding_connection_model`
REMOTE WITH CONNECTION `projects/gen-ai-igngar/locations/us/connections/llm_conn`
OPTIONS(ENDPOINT = 'textembedding-gecko@003');


CREATE OR REPLACE TABLE `conference_connect.embeddings` AS
SELECT * FROM ML.GENERATE_EMBEDDING(
  MODEL `conference_connect.embedding_connection_model`,
  (
    SELECT Interests,JobTitle,GCPProjects as content 
    FROM `conference_connect.attendees`
    LIMIT 3
  )
)
WHERE LENGTH(ml_generate_embedding_status) = 0;

#select count (*) from `conference_connect.embeddings`;

SELECT query.query, base.content
FROM VECTOR_SEARCH(
  TABLE `conference_connect.attendees`, 'ml_generate_embedding_result',
  (
  SELECT ml_generate_embedding_result, content AS query
  FROM ML.GENERATE_EMBEDDING(
  MODEL `conference_connect.embedding_connection_model`,
  (SELECT 'SQL' AS content))
  ),
  top_k => 5, options => '{"fraction_lists_to_search": 0.01}')
