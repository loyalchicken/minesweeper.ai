import {
  SHOW_SINGLE_REQUEST_DATA
} from "../actions/actionTypes";

const initialState = {
  activeTab: "Get"
};

export default function componentsReducer(state = initialState, action) {
  switch (action.type) {
    case SHOW_SINGLE_REQUEST_DATA:
      return {
        ...state
      };
    default:
      return state;
  }
}