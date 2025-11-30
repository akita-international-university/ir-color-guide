# IRデータ可視化配色ガイドライン

> [!IMPORTANT]
> 本リポジトリは現在作成中です。ここに記載されている内容は最終版ではなく、国際教養大学インスティテューショナル・リサーチ部門の公式な方針や慣行を示すものではありません。インスティテューショナル・リサーチ部門から明示的な許可を得ることなく、本リポジトリの内容を引用または配布しないでください。

## 目的

本ドキュメントの目的は、国際教養大学（AIU）アカデミックオフィスのインスティテューショナル・リサーチ部門（IR）が作成する成果物において、パレット（データ可視化に使用される色のセット）に関する明確な方針と慣行を定義することにより、一貫性、視認性、およびアクセシビリティを確保することです。

## 適用範囲

ダッシュボード、レポート、プロット、プレゼンテーション資料を含む（ただしこれらに限定されない）、IRチームが作成するすべての可視化データ。

## 方針

パレットは、AIUのウェブアクセシビリティ方針（[ウェブアクセシビリティ方針 | 公立大学法人 国際教養大学 | Akita International University](https://web.aiu.ac.jp/web-accessibility-policy/)）に準拠して設定する必要があります。基本的に、AIUのウェブアクセシビリティ方針は、Web Content Accessibility Guidelines（WCAG）の最新安定版に沿って定められています。

可能な限り、パレットはRの[`RColorBrewer`パッケージ](https://cran.r-project.org/web/packages/RColorBrewer/index.html)の色覚多様性対応パレットから選択する必要があります。これにより、IRチームが作成する資料が、受け手の色覚特性に関わらず理解可能であることを担保します。

## 技術的な注意事項

> [!NOTE]
> 本セクションを実行するには、[R（統計計算およびグラフィックスのための無料のオープンソースソフトウェア環境）](https://www.r-project.org/)のインストールが前提条件となります。

RColorBrewerの色覚多様性対応パレットは、Rコンソールで以下の簡単なコマンドを実行することで取得できます：

```r
# install.packages("RColorBrewer")
# または
# renv::install("RColorBrewer")
# 未インストールの場合
library(RColorBrewer)
RColorBrewer::display.brewer.all(colorblindFriendly = TRUE)
```

> [!TIP]
> [`tidyverse`パッケージ](https://tidyverse.org/)を使用している場合は、`RColorBrewer`を明示的に読み込む必要はありません。`library(tidyverse)`でtidyverseを読み込むだけで、そのセッション内で`RColorBrewer`が利用可能になります。

## 基本カラーパレットの定義

多くの可視化で使用される基本的なカラーパレットは、本リポジトリのルートにある設定ファイル`./palettes.yml`に事前定義されています。

このYAMLファイルに基づき、本リポジトリ内のPythonスクリプト`./scripts/build.py`がTableau設定ファイル`./tableau/Preferences.tps`およびRスクリプト`./r_script/ir_color_palettes.R`を生成します。これらのファイルは、それぞれのツールで可視化の配色に使用できます。

単一の設定YAMLファイルと、各ツール用に自動生成されるファイルのセットにより、IRチームが使用する複数のツール間での一貫性が確保されます。事前定義されたカラーパレットへのすべての変更は、個別のファイルではなくYAMLファイルに対して行う必要があります。

### パレットの使用方法

> [!IMPORTANT]
> 本セクションは現在空白です。TableauおよびRで生成されたカラーパレットを使用する方法については、今後のアップデートで追加される予定です。
