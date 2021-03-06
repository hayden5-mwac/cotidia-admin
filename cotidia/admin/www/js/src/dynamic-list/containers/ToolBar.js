import { connect } from 'react-redux'

import {
  cacheFilterLabel,
  clearFilters,
  manageColumns,
  performBatchAction,
  setFilterValue,
  setSearchTerm,
  switchMode,
  toggleSidebar,
} from '../redux/modules/search/actions'

import {
  anyResultsSelected,
  getToolbarFilters,
} from '../redux/modules/search/selectors'

import { getSuggestEngine } from '../utils/filterSuggestEngines'

import ToolBar from '../components/ToolBar'

const mapStateToProps = (state) => {
  const props = {
    allowedResultsModes: state.search.allowedResultsModes,
    anyResultsSelected: anyResultsSelected(state),
    batchActions: state.search.batchActions,
    columnsConfigurable: state.config.columnsConfigurable,
    filterConfiguration: state.search.filterConfiguration || {},
    filters: state.search.filters,
    hasSidebar: state.search?.sidebarFilters.length > 0,
    getSuggestEngine,
    resultsMode: state.search.resultsMode,
    toolbarFilters: getToolbarFilters(state),
  }

  if (state.search?.filterSuggestConfiguration?.mode) {
    props.filterSuggest = getSuggestEngine(
      state.search.filterSuggestConfiguration,
      state.search.filterConfiguration,
      true
    )
  } else {
    props.searchVisible = state.config.searchVisible
    props.searchTerm = state.search.searchTerm
  }

  return props
}

const actionCreators = {
  cacheFilterLabel,
  clearFilters,
  manageColumns,
  performBatchAction,
  setFilterValue,
  setSearchTerm,
  switchMode,
  toggleSidebar,
}

export default connect(mapStateToProps, actionCreators)(ToolBar)
