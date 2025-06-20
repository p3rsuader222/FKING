@echo off
cd D:\relocationasonedrive\LEARNCODE\Git_Finejas\pricing-insights-portfolio
mkdir data notebooks reports scripts powerbi docs
echo. > data\.gitkeep
echo. > notebooks\.gitkeep
echo. > reports\.gitkeep
echo. > scripts\.gitkeep
echo. > powerbi\.gitkeep
echo. > docs\.gitkeep
git add .
git commit -m "Add project folder structure with .gitkeep files"
git push origin main
git status