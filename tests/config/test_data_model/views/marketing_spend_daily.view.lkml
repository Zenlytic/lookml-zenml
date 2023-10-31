view: marketing_spend_daily {
  sql_table_name: `etl.prod_read_replica.marketing_spend_daily`
    ;;

  dimension_group: date {
    hidden: yes
    type: time
    description: "%m/%d/%E4Y"
    timeframes: [
      raw,
      date,
      week,
      month,
      quarter,
      year
    ]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.Date ;;
  }

  dimension: concat_primary_key {
    primary_key: yes
    hidden: yes
    type: string
    sql:${TABLE}.Media_Spend___Total || '-' ||  ${TABLE}.Date   ;;
  }

  dimension: media_spend___total {
    type: number
    sql: ${TABLE}.Media_Spend___Total ;;
  }

  measure: sum_daily_media_spend {
    label: "Daily Media Spend "
    type: sum_distinct
    sql: ${media_spend___total}  ;;
    value_format_name: usd
  }

}