# generative-ai-clean-architecture
生成AIをDDDで堅牢に扱うための自作基盤ライブラリ


# Overview
本リポジトリは、生成AI（LLM, TTS, Image Generation等）をエンタープライズレベルのアプリケーションに組み込むための、DDD（ドメイン駆動設計）に基づいた基盤ライブラリの実装サンプルです。
生成AIという「出力が不確実」かつ「進化が速い」外部要素を、ドメインロジックから完全に切り離し、保守性と交換可能性を最大化することを目的としています。


# Core Philosophies
* Dependency Inversion (DIP): AIモデル（Gemini, OpenAI等）を具体的なインフラストラクチャとして扱い、ドメイン層はインターフェースのみに依存します。
* Multi-Modal Orchestration: テキスト生成、音声合成、画像生成などの異なるモーダルを、ユースケース層で一貫したワークフローとして統合。
* Quality Assurance by ML: 生成物の品質を担保するため、BigQuery ML等を活用した自動検閲・乖離チェックの実装パターンを提供。


# Architecture & Tech Stack
オニオンアーキテクチャを採用し、各層の責務を明確に分離しています。

- **Design Pattern:** Domain-Driven Design (DDD)
- **AI Integration:** Google Gemini 2.5 (Pro/Flash), Cloud Text-to-Speech, BigQuery ML
- **Infrastructure:** Google Cloud Storage
    - BigQuery
    - BigQuery ML
    - Cloud Function
    - Vertex AI
    - Cloud Schedule
    - IAM
    - Cloud Storage
    - Workflows
- **Etc:**
    - Docker-Compose
    - DevContainer
    - GitHub Actions
    - FastAPI
    - Postgres

# 🤖 AI Model Abstraction / 🛡️ Grounding & QA Pipeline
Gemini Grounding を活用した事実基づく生成に加え、BigQuery ML を用いた事後検証ロジックをインターフェース化。生成AI特有の「ハルシネーション」をシステム構造的に抑制します。


# ⚙️ Flexible DI Container
punq などのDIコンテナ（または自作コンテナ）を用い、Local/Dev/Prod環境ごとに、実際のAI APIとMockを容易に切り替えられる構造を実現しています。

# Directory Structure
DDD ドメイン駆動設計に則り実装を行っています。
```text
tree src/ -d
src/
├── main.py                   # FastAPIよりHTTPリクエストを受け取る
├── application
│   └── usecases              # AIオーケストレーションのシナリオを記述
├── config
│   ├── db_config
│   └── di
├── domain
│   ├── interface             # AIサービスやリポジトリの抽象定義
│   │   ├── external_services
│   │   └── persistence
│   │       ├── database
│   │       └── storage
│   └── models                # AIに関わらない純粋なドメイン知識
└── infrastructure
    ├── external_services     # Gemini / TTS 等の具体的実装
    └── persistence           # BigQuery ML / ORM 等の実装
        ├── database
        ├── orm_models
        └── storage
```


# 🚀🚀🚀 Future Roadmap: Feedback Loop & Performance Prediction

生成したアセットのパフォーマンスデータを蓄積し、次回の生成プロセスにフィードバックする学習サイクルの構築を予定しています。


## 📊 Performance-Based Learning Pipeline
アセット公開後の「評価指標（エンゲージメント率等）」をデータウェアハウスへフィードバックし、高精度なアセット生成を実現するための予測モデルを構築します。

* **Data Engineering (Batch/Stream):**
    * 配信済みデータのパフォーマンス推移を収集し、BigQuery へ統合。
    * 大規模データの加工・前処理には **Apache Beam (Dataflow)** の導入を検討中。
* **Predictive Modeling (BigQuery ML):**
    * 過去の「ヒットアセット」の傾向を学習。
    * **Models:** `LOGISTIC_REGRESSION` または `BOOSTED_TREE_CLASSIFIER` を採用予定。
    * **Features:** 配信カテゴリ、メタデータの構成、配信タイミング、コンテンツの長さ等の特徴量から「ターゲット指標への到達確率」を予測します。
* **Optimization:**
    * 予測スコアが高いデータソースのみを優先的に抽出（Priority Queue化）し、パイプライン全体の ROI を最大化します。


## 📈 Data Visualization & Monitoring (Business Intelligence)
パイプラインの稼働状況および、生成したアセットのパフォーマンスを可視化し、継続的な改善サイクル（PDCA）を回すための基盤を構築します。

* **BI Tool Integration:**
    * **Looker Studio** を活用したリアルタイムダッシュボードの構築。
* **Key Metrics (KPIs):**
    * **System Health:** 各生成フェーズ（LLM/TTS/Image）の成功率、処理時間、APIコストの推移。
    * **Asset Performance:** 予測スコアと実際のエンゲージメント指標（KPI）の相関分析。
    * **Trend Analysis:** 特定のカテゴリや時間帯における「ヒット確率」の推移。
* **Objective:**
    * 数値に基づいたプロンプトの微調整や、特徴量の選定、リソース配分の最適化を迅速に行える環境を実現します。