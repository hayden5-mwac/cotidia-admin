import { connect } from 'react-redux'

import {
  clearFilter,
  configureFilter,
  moveColumn,
  setOrderColumn,
  toggleOrderDirection,
  toggleSelectAllResults,
} from '../../../redux/modules/search/actions'

import {
  getVisibleColumnConfig,
  getActiveFilters,
  allResultsSelected,
} from '../../../redux/modules/search/selectors'

import ResultsTableHeader from '../../../components/results/table/ResultsTableHeader'

const mapStateToProps = (state) => ({
  allSelected: allResultsSelected(state),
  batchActions: state.search.batchActions,
  categoriseBy: state.search.categoriseBy,
  columns: getVisibleColumnConfig(state),
  filters: getActiveFilters(state),
  orderAscending: state.search.orderAscending,
  orderColumn: state.search.orderColumn,
})

const actionCreators = {
  clearFilter,
  configureFilter,
  moveColumn,
  setOrderColumn,
  toggleOrderDirection,
  toggleSelectAllResults,
}

export default connect(mapStateToProps, actionCreators)(ResultsTableHeader)
