Very basic overview of Redux that's paraphrased from 'redux.js.org'-- the following info should be used to get a very basic overview of what's the purpose of the code in this folder.

## `Redux`
The Redux architecture revolves around a strict unidirectional data flow, meaning that all data in the application follows the same lifecycle pattern. Using Redux inside one's React app is a very popular combination because it helps to make state mutations a more predictable process by imposing restrictions on when and how state updates can happen. 

## `Actions`
Actions are payloads of information that send data from the application to the store. They are the only source of information for the store, and these payloads are sent via <code>store.dispatch()</code>. Actions are JavaScript objects that must have a <code>type</code> property, typically a string constant, that indicates the type of action being performed. 

## `Reducers`
Reducers specify how the application's state changes in response to actions sent to the store. Actions only describe what happened, but not how the application's state actually changes. Given some arguments, the reducer's job is to determine the next state and return it. 

## `Store`
The store is the object that brings together the actions and the reducers. The store holds the application state, allows access to state via <code>getState</code>, allows state to be updated via <code>dispatch(action)</code>, and registers/unregisters listeners via <code>subscribe(listener)</code>.
