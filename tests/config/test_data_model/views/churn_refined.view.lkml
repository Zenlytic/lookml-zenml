include: "/views/churn.view.lkml"

view: +churn {

  measure: total_churns {
    type: sum
    sql: ${churn} ;;
  }

  
}
