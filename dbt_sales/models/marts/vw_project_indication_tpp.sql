with vw_project_indication_tpp
as
(
WITH max_time_id AS (
  SELECT
    ind_unique_cd,
    MAX(time_id) AS max_time_id
  FROM
    srv_rnd_df.vw_indication
  WHERE
    NOT ind_shortname IS NULL
  GROUP BY
    ind_unique_cd
),
latest_indication AS (
  SELECT
    indrdpm.ind_unique_cd,
    indrdpm.ind_shortname,
    indrdpm.time_id
  FROM
    srv_rnd_df.vw_indication AS indrdpm
    JOIN max_time_id ON indrdpm.ind_unique_cd = max_time_id.ind_unique_cd
    AND indrdpm.time_id = max_time_id.max_time_id
)

SELECT
  tpp.tpp_prof_id as TPP_SYS_ID,
  tpp."Project Code" as PROJECT_CODE,
  case when latest_indication.ind_unique_cd is null then tpp.indication
  else latest_indication.ind_unique_cd end as INDICATION_UNIQUE_CODE,
  tpp.title as TPP_SOC_CATEGORY,
  tpp."Attribute Name" as TPP_SOC_SUBCATEGORY,
  tpp."Base Profile" as TPP_BASE_PROFILE_SOC_FOR_SUBCATEGORY,
  tpp."Upside Profile" as TPP_UPSIDE_PROFILE_SOC_FOR_SUBCATEGORY,
  tpp."Minimally Marketable Profile" as TPP_MINIMALLY_MARKETABLE_PROFILE_SOC_FOR_SUBCATEGORY,
  tpp."SOC Launch Name" as TPP_COMPARATOR_PRODUCT1_NAME,
  tpp."SOC Description" as TPP_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
  tpp."Comparative Position" as TPP_BASE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
  tpp."upside vs soc" as TPP_UPSIDE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
  tpp."minimally vs soc" as TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT1_SOC_FOR_SUBCATEGORY,
  tpp."SOC Launch Name 2" as TPP_COMPARATOR_PRODUCT2_NAME,
  tpp."SOC Description 2" as TPP_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
  tpp."Comparative Position 2" as TPP_BASE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
  tpp."Upside vs SOC 2" as TPP_UPSIDE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
  tpp."Minimally vs SOC 2" as TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT2_SOC_FOR_SUBCATEGORY,
  tpp."SOC Launch Name 3" as TPP_COMPARATOR_PRODUCT3_NAME,
  tpp."SOC Description 3" as TPP_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
  tpp."Comparative Position 3" as TPP_BASE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
  tpp."Upside vs SOC 3" as TPP_UPSIDE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
  tpp."Minimally vs SOC 3" as TPP_MINIMALLY_MARKETABLE_VS_COMPARATOR_PRODUCT3_SOC_FOR_SUBCATEGORY,
  tpp.status as TPP_STATUS,
  tpp.created as TPP_CREATED_DATE,
  tpp.modified as TPP_MODIFIED_DATE
  
FROM
  crdh_dea_iport_reporting.prtfl_tpp_profile AS tpp
  LEFT JOIN latest_indication ON tpp.indication = latest_indication.ind_shortname
  AND LEFT (
    latest_indication.ind_unique_cd,
    LENGTH (latest_indication.ind_unique_cd) - 7
  ) = tpp."Project Code"
where tpp.indication is not null  
ORDER BY
  tpp.tpp_prof_id)

SELECT * FROM vw_project_indication_tpp