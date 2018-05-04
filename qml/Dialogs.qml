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
                ProgressCircle {
                    id: progresscircle
                    y: parent.height / 2 - height / 2
                        size: parent.width / 10
                        colorCircle: status
                        colorBackground: "#E6E6E6"
                        arcBegin: 0
                        arcEnd: 360
                        lineWidth: size / 10
                    }
                Label {
                    x: progresscircle.x + progresscircle.width / 2 - width / 2
                    y: parent.height / 2 - height / 2
                    text: timestamp
                    font.pixelSize: mainWindow.width / 25
                }

                Image {
                    id: profileImage
                    source: data_dir + "/Pictures/Profiles/" + chat_identification + ".jpg"
                    asynchronous: true
                    height: parent.height
                    width: parent.width / 4
                    x: progresscircle.x + progresscircle.width
                }

                Label {
                    text: name
                    x: profileImage.x + profileImage.width//window.width / 2 - width / 2
                    y: parent.height / 2 - height / 2
                    font.pixelSize: mainWindow.width / 20
                    //anchors.fill: parent
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            python.call('Main.main.SetChatPartner', [name, chat_identification], function () {});
                            timeDialogs.running = false
                            timeChat.running = true
                            view.push(frameChat)
                        }
                    }
                }
                Item {
                    property string chatIdentification : chat_identification
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
