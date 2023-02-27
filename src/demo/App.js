/* eslint no-magic-numbers: 0 */
import React, {Component} from 'react';

import { MolstarViewer } from '../lib';

class App extends Component {

    constructor() {
        super();
        this.state = {
            value: 'dash'
        };
        this.setProps = this.setProps.bind(this);
    }

    setProps(newProps) {
        this.setState(newProps);
    }

    render() {
        return (
                <MolstarViewer id='viewer' layout={{layoutShowControls: true}} style={{ width: '100%', height: '800px' }}
                    setProps={this.setProps}
                    {...this.state}
                />
        )
    }
}

export default App;
