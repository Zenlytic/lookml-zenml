view: support_interactions {
  sql_table_name: `prod.support_interactions` ;;
  required_access_grants: [my_access_grant]

  dimension: totalcalltime {
    label: "Total Call Time"
    type: number
    sql: ${TABLE}.totalcalltime ;;
  }
  dimension: totalholdtime {
    label: "Total Hold Time"
    type: number
    sql: ${TABLE}.totalholdtime ;;
  }

  dimension: confidence_score {
    label: "Confidence Score"
    description: "The confidence level (0-1) for identifying the customer's reason for calling."
    type: string
    sql: ${TABLE}.confidence_score ;;
  }
  
  dimension: call_ticket_name {
    label: "Call ticket name"
    type: string
    sql: ${TABLE}.call_ticket_name ;;
  }
  
  
  measure: total_count {
    label: "Call Count"
    type: count
    sql: ${TABLE}.call_id ;;
    filters: {
      field: totalholdtime
      value: 1
    }
  }


}
