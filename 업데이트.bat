@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo   재고 대시보드 업데이트
echo ==========================================
echo.

cd /d %~dp0

echo [1/3] SAP 파일에서 데이터 추출 중...
python make_json.py
if errorlevel 1 (
    echo 오류 발생! 종료합니다.
    pause
    exit /b
)

echo.
echo [2/3] GitHub에 업로드 중...
git add data.json index.html
git commit -m "재고 데이터 업데이트 %date%"
git push

echo.
echo ==========================================
echo   완료! 브라우저에서 새로고침 하세요.
echo   https://tjdah4865-tech.github.io
echo ==========================================
echo.
pause
