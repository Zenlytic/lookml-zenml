view: churn {
  sql_table_name: `prod.churn_details` ;;

  dimension: account_id {
    type: string
    sql: ${TABLE}.acct_id ;;
  }

  dimension: churn {
    type: number
    sql: ${TABLE}.churn_flag ;;
  }
}
