## Generate IAM access key for setting of credentials that allow API requests to be made as an IAM user.
gpg --gen-key
gpg --armor --export <your_email@example.com> > public_key.asc

## Login to GEEKSNIPE Organisation
```shell
pulumi login
```

---

## AWSのプロファイルの指定
```shell
export AWS_PROFILE=geeksnipe-dev
```

---

## スタックの作成

```shell
pulumi stack new
```

---

## pulumiでスタックの選択

![スクリーンショット 2023-12-27 9 58 12](https://github.com/kouhei-github/serverless-geeksnipe.com/assets/49782052/24c95621-64e3-4872-b90c-0d768adf1f2b)


```shell
pulumi stack select kohei/geeksnipe/mysql
```

---

## Set config secret
```shell
# pulumi config set --secret <AWSリージョン> <AWSリージョン名> # 下記が例
pulumi config set aws:region ap-northeast-1
```

---

## Run the program to update the stack
```shell
pulumi up
```

---
