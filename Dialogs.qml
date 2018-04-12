import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width


    function antwortGetDialogs(item) {
        console.warn("test")
        console.warn("log")

        dialogsModel.clear()

        for (var i=0; i<item.length; i++) {
            dialogsModel.append(item[i]);
        }
    }

    Label {
        id: labelSelectTitle
        text: "Telepygram"
        font.pixelSize: mainWindow.width / 20
        x: mainWindow.width / 2 - width / 2
    }


    ListView {
        id: listeDialogs
        y: window.height / 20
        width: window.width
        height: window.height * 0.5

        ListModel {
            id: dialogsModel
        }

        Component {
            id: dialogsDelegate
            Item {
                id: itemListe
                width: window.width
                height: window.height/6
                MouseArea {
                    anchors.fill: parent
                    onClicked: liste.currentIndex = index
                }
                Label {
                    text: "Test"
                    anchors.fill: parent
                }
            }
        }

        model: dialogsModel
        delegate: dialogsDelegate
    }


}
