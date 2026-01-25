-- ドメインに対する人気予想指数の算出クエリ
BEGIN
  -- 1. 設定値を格納する変数を宣言
  DECLARE v_temperature FLOAT64;
  DECLARE v_max_output_tokens INT64;

  -- 2. 設定値をテーブルから取得
  SET (v_temperature, v_max_output_tokens) = (
    SELECT AS STRUCT 
      temperature, 
      max_output_tokens
    FROM `****.****.prompt_management`
    WHERE task_id = '****_trend_analysis' AND is_active = TRUE
    ORDER BY version DESC LIMIT 1
  );

  EXECUTE IMMEDIATE FORMAT("""
    INSERT INTO `****.****.****_trend_scores` (
      ****_id,
      ****_at,
      buz_score,
      buz_reason
    )
    WITH active_prompt AS (
      SELECT * FROM `****.****.prompt_management`
      WHERE task_id = '****_trend_analysis' AND is_active = TRUE
      ORDER BY version DESC LIMIT 1
    ),
    input_data AS (
      SELECT 
        p1.****_id,
        p1.****_at,
        REPLACE(ap.prompt_template, '{{title}}', p1.title) AS prompt
      FROM 
        `****.****.raw_****s` p1
      CROSS JOIN 
        active_prompt ap
      LEFT JOIN 
        `****.****.****_trend_scores` p2 ON
        p1.****_id = p2.****_id
        AND TIMESTAMP_TRUNC(p2.****_at, DAY) = TIMESTAMP(CURRENT_DATE)
      WHERE 
        p2.****_id IS NULL
      AND TIMESTAMP_TRUNC(p1.****_at, DAY) = TIMESTAMP(CURRENT_DATE)
    ),
    raw_response AS (
      SELECT
        ****_id,
        ****_at,
        -- AI.GENERATE_TEXT の結果テキストは 'result' カラムに格納されている
        -- マークダウンの ```json と ``` を除去する
        REGEXP_REPLACE(result, r'^```json\\n|```\\n?$', '') AS cleaned_json
      FROM
        AI.GENERATE_TEXT(
          MODEL `****.****.gemini_flash_****`,
          (SELECT ****_id, ****_at, prompt FROM input_data),
          STRUCT(
            %f AS temperature,
            %d AS max_output_tokens
          )
        )
    )
    SELECT
      ****_id,
      ****_at,
      SAFE_CAST(JSON_VALUE(SAFE.PARSE_JSON(cleaned_json), '$.score') AS INT64) AS buz_score,
      JSON_VALUE(SAFE.PARSE_JSON(cleaned_json), '$.reason') AS buz_reason
    FROM raw_response;
  """, v_temperature, v_max_output_tokens);
END;



