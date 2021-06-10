/*
Used to test the buttons
*/
import React from 'react'
import Btn from './RemoveButton'

const mockTeamPage = () => {
    const userinfo = '1';
    const remove = (i) => {

        fetch("\remove", {
            methods: ["POST"],
            body: JSON.stringify({
                uid: this.state.uid[i],
                tid: this.state.tid,
            }),}
        ).then(response => response.json()
        ).then(json => {
            this.state.uid.splice(i,1)
        });

    }
    this.state = {uid: [uid], tid: tid}
    Return (
        <>
            <Btn backgroundColor=Red text='remove' onClick={() => remove(1)}/> // uid
        </>
    )
}