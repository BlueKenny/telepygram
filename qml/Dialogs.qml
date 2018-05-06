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

    Rectangle {
        id: topPanelDialog
        width: window.width
        height: appTitle.height + 40
        z: 1
    }

    Label {
        id: appTitle
        text: "Telepygram"
        x: mainWindow.width / 2 - width / 2
        y: 20
        z: 2
        font.pixelSize: mainWindow.width / 20
    }

    ListView {
        id: listeDialogs
        y: topPanelDialog.height
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
                    /*
                    onStatusChanged: {
                        console.warn("Image Status " + status + " of " + name)
                        console.warn("Progress " + progress)
                        if (status == 3) {
                            if (progress == 1) {
                                python.call('Main.main.deleteProfilePhoto', [chat_identification], function () {});
                            }
                        }
                    }*/
                }

                Label {
                    text: name
                    x: profileImage.x + profileImage.width//window.width / 2 - width / 2
                    y: parent.height / 2 - height / 2
                    font.pixelSize: mainWindow.width / 20
                    //anchors.fill: parent
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        python.call('Main.main.SetChatPartner', [name, chat_identification], function () {});
                        timeDialogs.running = false
                        timeChat.running = true
                        view.push(frameChat)
                        python.call('Main.main.reloadChat', [true], function () {});
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
