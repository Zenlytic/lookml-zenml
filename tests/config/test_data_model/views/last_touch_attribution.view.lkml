view: last_touch_attribution_view {
  sql_table_name: `etl.prod_read_replica.last_touch_attribution_2_view`
    ;;

  dimension: profile_id {
    hidden: yes
    primary_key: yes
    description: "Unique ID assigned to each order"
    type: number
    sql: ${TABLE}.profile_id ;;
  }

  dimension: psession_id {
    hidden: yes
    description: "Psession that follows user through their experience"
    type: number
    sql: ${TABLE}.psession_id ;;
  }

  dimension: utm_campaign {
    description: "Campaign that user was tracked from"
    type: string
    sql: ${TABLE}.utm_campaign ;;
  }

  dimension: utm_content {
    description: "Content in the source/campaign followed by user"
    type: string
    sql: ${TABLE}.utm_content ;;
  }

  dimension: utm_medium {
    description: "Medium which the user recieved the campaign/source"
    type: string
    sql: ${TABLE}.utm_medium ;;
  }

  dimension: utm_source {
    description: "Source that the user was tracked from"
    type: string
    sql: ${TABLE}.utm_source ;;
  }

  dimension: utm_term {
    hidden: yes
    type: string
    sql: ${TABLE}.utm_term ;;
  }

  measure: count {
    label: "Profiles From UTM"
    description: "Count of Profiles attributed from source"
    type: count
    drill_fields: [profile_id]
  }
}