![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)
![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)
![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)


# Snapsheets

Wget snapshots of Google Spreadsheets

This package enables to wget Google Spreadsheets without login.
(Spreadsheets should be shared with public link)


---

# Usage

```python
>>> import snapsheets as ss
>>> ss.add_config('test_config.yml')
>>> ss.get('test1', by='wget')
```

---

## Config

- Write config file in ``YAML`` format

```yaml
volumes:
  snapd: 'data/'

options:
  wget:
    '--quiet'

sheets:
  test1:
    key: '1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM'
    gid: 'None'
    format: 'xlsx'
    sheet_name:
      - 'シート1'
      - 'シート2'
    stem: 'test_sheet'
    datefmt: '%Y'
```

---

# Documents

- https://shotakaha.gitlab.io/snapsheets/

---

# Snapsheets

Wget snapshots of Google spreadsheet

---

![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)
![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)
![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)

---

![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)

---

# Usage

```python
>>> import snapsheets as ss
>>> ss.add_config('config.yml')
>>> ss.get('test1', by='wget')
```

# Install

```bash
$ pip3 install snapsheets
```

# Documents

- https://shotakaha.gitlab.io/snapsheets/

---

# 設定ファイルの項目

- ``volumes`` : 保存先
- ``options`` : ダウンロード時のオプション
- ``sheets`` : スプレッドシートの情報

## ``volumes`` : 保存先

- ダウンロードしたスプレッドシートを保存する場所を設定する項目
- いまは ``snapd`` だけ必要
- デフォルトはカレントディレクトリ

```yaml
volumes:
  snapd: "."
```

## ``options`` : ダウンロード時のオプション

- ダウンロード時のオプションを設定する項目
- いまは ``wget`` だけ必要

```yaml
options:
  wget:
    '--quiet'
```

## ``sheets`` : スプレッドシートの情報

- スプレッドシートの情報を設定する項目
- 複数のスプレッドシートを設定できる

```yaml
sheets:
  シートの名前:
    key: スプレッドシート全体のID
    gid: ダウンロードするシートのID
    format: ダウンロード形式
    sheet_name:
      - 'シートの名前'
    stem: 'バックアップ時につけるファイル名'
    datefmt: 'バックアップ時に使う日付フォーマット'
```

### ``datefmt`` : 日付フォーマット

- バックアップする際のファイル名につける日付プリフィックス
- デフォルトは ``%Y%m%dT%H%M%S``


---


# 開発用メモ

## ローカルでテストする場合

```bash
$ git clone https://gitlab.com/shotakaha/snapsheets.git
$ cd snapsheets/python/
$ pip3 install .
$ pip3 show snapsheets
```

## Test PyPI のテストをする場合

```bash
$ pip3 install -i https://test.pypi.org/simple/
$ pip3 show snapsheets
```


---

# Test PyPI への登録

- https://test.pypi.org/project/snapsheets/
- API Token を発行する
  - ``API Token``は一度しか発行できない（忘れてしまったら再発行するしかない？）
  - ``$HOME/.pypirc``に設定を保存しておく

## アップロード

```bash
$ cd python/
$ rm -r dist/
$ python3 setup.py sdist bdist_wheel
$ twine upload --repository testpypi dist/*
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: __token__
Enter your password: ## APIトークンをコピペ
```

---

# PyPI への登録

- https://pypi.org/project/snapsheets/
- API Token を発行する
  - ``API Token``は一度しか発行できない（忘れてしまったら再発行するしかない？）
  - ``$HOME/.pypirc``に設定を保存しておく

## アップロード

```bash
$ cd python/
$ rm -r dist/
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/*
Uploading distributions to https://pypi.org/legacy/
```

---

# ``$HOME/.pypirc`` の設定

- 以下の記事を参照
- https://truveris.github.io/articles/configuring-pypirc/

```conf
[distutils]
  index-servers=
      pypi
      testpypi

[testpypi]
  repository: https://test.pypi.org/legacy/
  username = __token__
  password = pypi-****

[pypi]
  username = __token__
  password = pypi-****
```

---

## ``TestPyPI``にアップロードしたときに分かったこと／気をつける点

- メールアドレス（``setup.py``に書く``author_email``）は、``TestPyPI``に登録したメールアドレスでなくてもOKだった
  - ``valid``な文字列であればなんでもよいみたい
  - ``invalid``なアドレスは``twine``でエラーがでる（``xxxxxx``にしてたら怒られた）
- 同じ名前のファイルは登録することができない
  - https://test.pypi.org/help/#file-name-reuse を参照
  - ``twine upload``する前に ``dist/*`` を空っぽにしたほうがよい
  - リビジョン番号は、当面``Test PyPi``の表示確認ように使うことにする
