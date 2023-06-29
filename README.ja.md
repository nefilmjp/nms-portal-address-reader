# No Man's Sky Portal Address Reader

[English](README.md) | **日本語**

OpenCVを使用してスクリーンショットからポータルアドレスを読み取る。

- 不安定版
- 解像度は1920x1080のみ対応
- 以下の内容を出力する
    - カンマ区切りの12個の整数
    - 12桁の16進数（ポータル文字フォント用）
    - 結果確認用のスクリーンショットの切り抜きと読み取り結果の比較画像

## 使用方法

- `config.sample.ini` を `config.ini` としてコピーする
- OSに `OpenCV` ・ `Python` ・ `pipenv` をインストールする
    - Debian/Ubuntuの場合OpenCVは `libopencv-dev` パッケージを使用する
- `pipenv install` で依存関係をインストールする
- ポータルアドレスを含む1920x1080のスクリーンショットを `screenshots` ディレクトリに格納する
    - 標準で対象となるのは `screenshots/*.jpg`
- `pipenv run main`
    - 出力をファイルに保存したい場合は `pipenv run main > result.txt` 等とする
- 目視確認用の画像が `result.jpg` に出力される
