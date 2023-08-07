// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, {Fragment} from 'react';
import { ErrorJSON } from '../widget';

// import css
import "../../css/margins.css"

import DefaultModal from './DefaultModal'; 
import { ModalEnum, ModalInfo } from './Mito';
import EasterIcon from './icons/EasterIcon';

/*
    A modal that displays error messages and gives
    users actions to recover.
*/
const ErrorModal = (
    props: {
        errorJSON: ErrorJSON, 
        setModal: (modalInfo: ModalInfo) => void
    }): JSX.Element => {

    let header = "Oops! " + props.errorJSON.header;
    let mailto = 'mailto:aarondr77@gmail.com';
    let to_fix = (
        <div>
            {props.errorJSON.to_fix} 
        </div>
    )
    // If it's an easter egg, we just display the egg!
    if (props.errorJSON.type === 'easter_egg') {
        header = props.errorJSON.header
        mailto = 'mailto:aarondr77@gmail.com?subject=Claiming my Easter Egg'
        to_fix = (
            <div style={{'display': 'flex', 'flexDirection': 'column'}}>
                <div>
                    {props.errorJSON.to_fix} 
                </div>
                {EasterIcon()}
            </div>
        )
    }

    return (
        <DefaultModal
            header={header}
            modalType={ModalEnum.Error}
            viewComponent={
                <Fragment>
                    {to_fix}
                </Fragment>
            }
            buttons={
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={() => {
                        window.open(mailto, '_blank');
                        props.setModal({type: ModalEnum.None});
                    }}> {"Contact Us"}
                    </div>
                </Fragment> 
            }
        />
    )    
};

export default ErrorModal;