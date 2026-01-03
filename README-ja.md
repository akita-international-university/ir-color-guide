<!-- markdownlint-disable MD013 -->

# IRデータ可視化配色ガイドライン

[Click here for the English version](./README.md)

> [!IMPORTANT]
> 本リポジトリは現在作成中です。ここに記載されている内容は最終版ではなく、国際教養大学における公式な方針や考えを示すものではありません。教学IRチームから明示的な許可を得ることなく、本リポジトリの内容を引用または配布することを禁止します。

## 目的

本ガイドラインは、国際教養大学（AIU）教務課教学IRチームが使用するパレット（データ可視化に使用される配色セット）に関する明確な方針を定義することで、教学IRチームの成果物における一貫性、視認性、およびアクセシビリティを担保することを目的としています。

## 適用範囲

本ガイドラインの適用範囲は、教学IRチームが作成するすべての可視化データです。これにはBIツール等で作成・更新されるダッシュボードやレポート、グラフ、プレゼンテーション資料などが含まれます。

## 方針

パレットは、AIUのウェブアクセシビリティ方針（[ウェブアクセシビリティ方針 | 公立大学法人 国際教養大学 | Akita International University](https://web.aiu.ac.jp/web-accessibility-policy/)）に準拠して設定することとします。さらに、AIUのウェブアクセシビリティ方針が、Web Content Accessibility Guidelines（WCAG）の最新版に沿って定められていることを前提に、同方針で明示されていない内容はWCAGを参照することとします。

教学IRチームが作成する資料が、受け手の色覚特性に関わらず理解できるものであることを担保するために、パレットは可能な限り、Rの[`RColorBrewer`パッケージ](https://cran.r-project.org/web/packages/RColorBrewer/index.html)の色覚多様性対応パレットから選択することとします。

> [!NOTE]
> 教学IRチームでは、作成するすべての可視化資料が色覚多様性に対応したものとなることを目指しているものの、利用可能なリソースの制約から、現時点では（必ずしも色覚多様性に対応していない）既存の資料の配色設定をそのまま使用しているものもあります。引き続き、資料のアクセシビリティ向上に向けて継続的に取り組んでいきますが、とりわけ色覚多様性対応を確保するためのチェックを自動化するための提案やフィードバックは歓迎です。

## 基本カラーパレットの定義

多くの可視化で使用される基本的なカラーパレットは、本リポジトリのルートにある設定ファイル`./palettes.yml`に事前定義されています。

このYAMLファイルに基づき、本リポジトリ内のPythonスクリプト`./scripts/build.py`が、Tableau設定ファイル`./tableau/Preferences.tps`およびRスクリプト`./r_script/ir_color_palettes.R`を生成します。これらのファイルは、それぞれのツールで可視化の配色に使用できます。

単一の設定YAMLファイルと、各ツール用に自動生成されるファイルをセットで管理することにより、教学IRチームが使用する複数のツール間での一貫性を担保します。事前定義されたパレットへのすべての変更は、個別のファイルではなくYAMLファイルに対して行うこととします。

### パレットの使用方法

> [!NOTE]
> 本セクション以降の説明では、[R（統計及び可視化のための無料のオープンソースソフトウェア環境）](https://www.r-project.org/)がインストール済みであることを前提としています。

#### R

本リポジトリで定義されたカラーパレットをRで使用する最も簡単な方法は、生成されたRスクリプト[`./r_script/ir_color_palettes.R`](./r_script/ir_color_palettes.R)を、作業中のRスクリプトやQuartoドキュメントでダウンロードして `source` で参照することです：

```r
# 作業中のファイル（例: analysis.R や report.qmd）にて
source("path/to/this/repository/r_script/ir_color_palettes.R")

# ggplot2での使用例:
df |>
  ggplot(aes(x = year, y = value, fill = category)) +
  geom_col() +
  scale_fill_manual(values = color_values_4scale_likert) # 事前定義されたパレットを使用
```

もしRスクリプトを手動でダウンロードせずに、最新バージョンを動的に参照する必要がある場合は、`source` のファイルパスをGitHub URLに置き換えてください：

```r
source("https://raw.githubusercontent.com/akita-international-university/ir-color-guide/refs/heads/main/r_script/ir_color_palettes.R")
```

上記の方法では、本リポジトリの `main` ブランチにあるRスクリプトの最新版が常に参照できる一方で、breaking changes (後方互換性のない変更) が導入された場合に、既存のコードが動作しなくなるリスクがあります。安定したバージョンを使用したい場合は、特定のコミットハッシュやタグを指定したURLを使用してください:

```r
# 特定のバージョン (v1.2.3) を参照する例
source("https://raw.githubusercontent.com/akita-international-university/ir-color-guide/refs/tags/v1.2.3/r_script/ir_color_palettes.R")
```

> [!TIP]
> 上記のうちどの方法を採るか分からない場合は、安定運用の観点から、取り急ぎ最後の方法（特定のバージョンを参照する方法）を使用することをお勧めします。

#### Tableau

カスタムカラーパレットは、Tableau Desktopのインストール時にローカルに作成される`Preferences.tps`ファイルを編集することで定義できます。本セクションでは、本リポジトリで生成された`Preferences.tps`ファイルを使用して、Windows PC上のTableau Desktopでカスタムカラーパレットを設定する方法を説明します。

> [!IMPORTANT]
> 以下の方法では、Tableauリポジトリ内の既存の`Preferences.tps`ファイルが上書きされます。現在ご利用中の`Preferences.tps`に独自のカスタムカラーパレットが定義されている場合は、作業前に必ずバックアップを作成してください。

> [!NOTE]
> Tableauでカスタムカラーパレットを作成する詳細な手順については、Tableau公式ドキュメント（[カスタムカラーパレットの作成](https://help.tableau.com/current/pro/desktop/ja-jp/formatting_create_custom_colors.htm)）をご参照ください。

1. Tableauリポジトリフォルダを探します。デフォルトでは、以下の場所にあります：
   ```
   C:\Users\<YourUsername>\Documents\My Tableau Repository
   ```
2. `My Tableau Repository`フォルダ内にある既存の`Preferences.tps`ファイルを見つけ、必要に応じてバックアップを作成してください。
3. 本リポジトリで生成された[`./tableau/Preferences.tps`](./tableau/Preferences.tps)ファイルを`My Tableau Repository`フォルダにコピーし、既存のファイルを置き換えます。
4. Tableau Desktopを起動中の場合は再起動してください。

## 技術的な留意事項

RColorBrewerの色覚多様性対応パレットは、Rコンソールで以下の簡単なコマンドを実行することで取得できます：

```r
# 未インストールの場合は、RColorBrewerパッケージをインストールしてください:
# install.packages("RColorBrewer")
# または
# renv::install("RColorBrewer")
library(RColorBrewer)
RColorBrewer::display.brewer.all(colorblindFriendly = TRUE)
```

> [!TIP]
> [`tidyverse`パッケージ](https://tidyverse.org/)を使用している場合は、`RColorBrewer`を明示的に読み込む必要はありません。`library(tidyverse)`でtidyverseを読み込むだけで、そのセッション内で`RColorBrewer`が利用可能になります。
