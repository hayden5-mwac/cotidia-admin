import { connect } from 'react-redux'

import { editField } from '../redux/modules/search/actions'

import ResultsTableItemValue from '../components/ResultsTableItemValue'

const mapStateToProps = (state, props) => ({
  config: state.config,
})

const actionCreators = { editField }

export default connect(mapStateToProps, actionCreators)(ResultsTableItemValue)
