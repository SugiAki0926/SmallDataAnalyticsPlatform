-- lake（環境共通）。dlt が書く。dbt は読むだけ。
CREATE SCHEMA raw;

-- dbt のデフォルト連結: {profiles.yml の schema}_{+schema}
-- 学習用に dev / prod を名前で明示する。
CREATE SCHEMA dev_staging;
CREATE SCHEMA dev_intermediate;
CREATE SCHEMA dev_marts;
CREATE SCHEMA dev_seed;
CREATE SCHEMA dev_snapshots;
CREATE SCHEMA prod_staging;
CREATE SCHEMA prod_intermediate;
CREATE SCHEMA prod_marts;
CREATE SCHEMA prod_seed;
CREATE SCHEMA prod_snapshots;
