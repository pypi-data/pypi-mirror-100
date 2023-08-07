// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useEffect, useState } from 'react';
import DefaultTaskpane from '../DefaultTaskpane';
import { MitoAPI } from '../../../api';

// Import 
import '../../../../css/import-taskpane.css'
import { TaskpaneInfo } from '../taskpanes';
import LargeSelect from '../../elements/LargeSelect';
import XIcon from '../../icons/XIcon';

interface ImportTaskpaneProps {
    mitoAPI: MitoAPI;
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
}

/* 
    Provides a live updating import modal
    that allows users to import data
*/
function ImportTaskpane(props: ImportTaskpaneProps): JSX.Element {

    // Save the step id for overwriting
    const [stepID, setStepID] = useState('');

    // The datafiles are the files loaded from the backend
    const [dataFiles, setDataFiles] = useState<string[]>([]);
    const [hasLoadedDataFiles, setHasLoadedDataFiles] = useState(false);

    // Which files are actually selected by the user
    const [selectedFiles, setSelectedFiles] = useState<string[]>([]);

    /* 
        Sends a message to the backend, importing files (and overwriting
        the step if it already exists).
    */
    async function sendImportMessage(files: string[]) {
        const newStepID = await props.mitoAPI.sendSimpleImportMessage(
            files,
            stepID
        )
        setStepID(newStepID);
    }

    /* 
        Loads the data files from the backend, and then
        initializes the imported files to the first file
        returned (if it exists). Aka, we default the user
        to importing one file.
    */
    async function getDataFiles() {
        // Loads the data files
        const receivedDataFiles = await props.mitoAPI.getDataFiles();
        setDataFiles(receivedDataFiles);
        // Save that we have loaded the files
        setHasLoadedDataFiles(true);

        // If there are any data files returned, then we by default
        // select one of them and import it
        if (receivedDataFiles.length > 0) {
            const defaultImports = [receivedDataFiles[0]];
            setSelectedFiles(defaultImports);
            await sendImportMessage(defaultImports);
        }
    }

    // Updates a specific imported file to a specific import
    const updateImportedFile = async (index: number, newImport: string): Promise<void> => {
        const newImports = [...selectedFiles];
        newImports[index] = newImport;
        setSelectedFiles(newImports);

        // Set a message to actually update this
        await sendImportMessage(newImports);
    }

    // Adds a new file to import
    const addNewFileImport = async (): Promise<void> => {
        const newImports = [...selectedFiles];

        // We take the first file that has not been imported, or if all files have been
        // imported, than just the first file
        let newImport = dataFiles[0];

        const unimportedFiles = dataFiles.filter(fileName => !selectedFiles.includes(fileName));
        if (unimportedFiles.length > 0) {
            newImport = unimportedFiles[0];
        }
        
        newImports.push(newImport);
        setSelectedFiles(newImports);

        // Send a message to actually update this
        await sendImportMessage(newImports);
    }

    // Removes a file from being imported
    const removeFileImport = async (index: number): Promise<void> => {
        const newImports = [...selectedFiles];
        newImports.splice(index, 1);

        setSelectedFiles(newImports);

        // Send a message to actually update this
        await sendImportMessage(newImports);
    }

    useEffect(() => {
        // We load the data after the component renders
        void getDataFiles();
    }, []) // empty array is necessary to have this run only once

    return (
        <DefaultTaskpane
            header = {'Import CSV Files'}
            setCurrOpenTaskpane={props.setCurrOpenTaskpane}
            taskpaneBody = {
                <React.Fragment>
                    {!hasLoadedDataFiles && 
                        // We display a loading message while loading the files from the backend
                        <div>
                            Loading data files in the current folder...
                        </div>
                    }
                    {hasLoadedDataFiles && dataFiles.length === 0 &&
                        // We display a loading message while loading the files
                        <div>
                            There are no files in the current folder to import. <br/> <br/>
                            
                            Upload files to this folder, and then reopen the import taskpane. <br/> <br/>
                            
                            You can read more about importing <a href='https://docs.trymito.io/getting-started/importing-data-to-mito' target="_blank" rel="noreferrer"><u>here.</u></a>
                        </div>
                    }
                    {hasLoadedDataFiles && dataFiles.length > 0 &&
                        // If we loaded some files, we let users import files
                        <React.Fragment>
                            {selectedFiles.map((fileName, i) => {
                                return (
                                    <div key={i} className='import-file-select-container'>
                                        <LargeSelect
                                            key={i}
                                            startingValue={fileName}
                                            optionsArray={dataFiles}
                                            setValue={(fileName) => {void updateImportedFile(i, fileName)}}
                                            extraLarge={true}
                                        />
                                        <div className='import-file-delete' onClick={() => {void removeFileImport(i)}}>
                                            <XIcon/>
                                        </div>
                                    </div>
                                )
                            })}
                            <div className='add-button' onClick={addNewFileImport}>
                                + Add Data File
                            </div>
                        </React.Fragment>
                    }
                </React.Fragment>
            }
        />
    )
}

export default ImportTaskpane;