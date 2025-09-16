include: "/views/support_interactions.view.lkml"
view: ext_support_interactions {
  extends: [support_interactions]
  extension: required


dimension: confidence_score {
  type: number
  sql: SAFE_CAST(${confidence_score} as NUMERIC) ;;
}

measure: total_unique_scores {
  type: count_distinct
  sql: ${confidence_score} ;;
}

dimension: avg_hold_time {
  type: average
  sql: ${totalholdtime} ;;
}
}
