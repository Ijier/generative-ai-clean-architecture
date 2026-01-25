-- 生成したデータとドメインの内容に乖離がないかのチェッククエリ
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
    WHERE task_id = '****_quality_check_analysis' AND is_active = TRUE
    ORDER BY version DESC LIMIT 1
  );

  EXECUTE IMMEDIATE FORMAT("""
    INSERT INTO `****.****.****_quality_check_analysis` (
      ****_id,
      ****_at,
      quality_check_score,
      analysis_summary
    )
    WITH active_prompt AS (
      SELECT * FROM `****.****.prompt_management`
      WHERE task_id = '****_quality_check_analysis' AND is_active = TRUE
      ORDER BY version DESC LIMIT 1
    ),
    input_data AS (
      SELECT 
        p1.****_id,
        p1.****_at,
        REPLACE(ap.prompt_template, '{{script_body}}', p1.script_body) AS prompt
      FROM 
        `****.****.****` p1
      CROSS JOIN 
        active_prompt ap
      LEFT JOIN 
        `****.****.****_quality_check_analysis` p2 ON
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
          MODEL `****.****.gemini_quality_evaluator`,
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
      SAFE_CAST(JSON_VALUE(SAFE.PARSE_JSON(cleaned_json), '$.score') AS INT64) AS quality_check_score,
      JSON_VALUE(SAFE.PARSE_JSON(cleaned_json), '$.reason') AS analysis_summary
    FROM raw_response;
  """, v_temperature, v_max_output_tokens);
END;



