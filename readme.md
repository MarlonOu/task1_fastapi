# 安裝說明
## 開發環境
請在``vscode``下開發，利用``pdm init``和``pdm install``完成虛擬環境建置

## 安裝包
這是一個devlop的模板樣式，已經安裝了下列package
* ruff
* black
* commitizen
* pre-commit
* pytest
* allure
```diff
- 請記得利用 cz init 初始化
! 請記得利用 pre-commit 導入自定義規則
```
# 注意事項
### 請記得設定``MS_TEAMS_WEBHOOK_URI``＆``ALLURE``的TOKEN