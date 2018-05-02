import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width


    function antwortGetDialogs(item) {
        dialogsModel.clear()

        for (var i=0; i<item.length; i++) {
            dialogsModel.append(item[i]);
        }
    }

    Timer {
        interval: 5000; running: true; repeat: true
        onTriggered: {
            console.warn("Timer")
            python.call('Main.main.reloadDialogs', [], function () {});
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
        y: window.height / 10
        width: window.width
        height: window.height * 0.8

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
                    text: name
                    x: window.width / 2 - width / 2
                    font.pixelSize: mainWindow.width / 20
                    //anchors.fill: parent
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            python.call('Main.main.SetChatPartner', [name], function () {});
                            view.push(frameChat)
                            python.call('Main.main.getChat', [], function () {});
                        }
                    }
                }
            }
        }

        model: dialogsModel
        delegate: dialogsDelegate
    }


    Python {
        id: python
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('./'));
            importModule('Main', function () {});

            setHandler("antwortGetDialogs", antwortGetDialogs);
        }
    }

}
