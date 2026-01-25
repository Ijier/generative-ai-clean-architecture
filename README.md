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

# 🤖 AI Model Abstraction

# 🛡️ Grounding & QA Pipeline
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