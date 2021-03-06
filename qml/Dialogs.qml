import QtQuick 2.2
import io.thp.pyotherside 1.2
import QtQuick.Controls 1.1//2.2
import QtGraphicalEffects 1.0

Rectangle {
    id: window
    height: mainWindow.height
    width: mainWindow.width
    color: vars.backgroundColor

    function antwortGetDialogs(item) {
        dialogsModel.clear()

        for (var i=0; i<item.length; i++) {
            dialogsModel.append(item[i]);
        }
    }

    Rectangle {
        id: topPanelDialog
        width: window.width
        height: appTitle.height * 2 + 40
        z: 1
        border.width: 2
        color: vars.backgroundColorPanel
        Label {
            id: appTitle
            text: "Telepygram"
            x: mainWindow.width / 2 - width / 2
            y: 20
            font.pixelSize: mainWindow.width / 20
            color: vars.textColor
        }

        Label {
            id: labelStatus
            text: vars.onlineStatus ? "You are\nOnline" : "You are\nOffline"
            color: vars.onlineStatus ? "green" : "red"
            x: window.width - width
            font.pixelSize: mainWindow.width / 28
            transform: Rotation { origin.x: 0; origin.y: 0; axis { x: 1; y: 1; z: 1 } angle: 45 }
        }
    }

    ListView {
        id: listeDialogs
        y: topPanelDialog.height
        width: window.width
        height: window.height * 0.8
        z: topPanelDialog.z - 1

        ListModel {
            id: dialogsModel
        }

        Component {
            id: dialogsDelegate
            Item {
                id: itemListe
                width: window.width
                height: window.height/10

                MouseArea {
                    anchors.fill: parent
                    onClicked: liste.currentIndex = index
                }/*
                ProgressCircle {
                    id: progresscircle
                    y: parent.height / 2 - height / 2
                        size: parent.width / 10
                        colorCircle: status
                        colorBackground: "#E6E6E6"
                        arcBegin: 0
                        arcEnd: 360
                        lineWidth: size / 10
                    }*/
                Label {
                    //x: progresscircle.x + progresscircle.width / 2 - width / 2
                    //y: parent.height / 2 - height / 2
                    text: "Offline: " + timestamp
                    font.pixelSize: dialogsName.font.pixelSize * 0.5
                    color: vars.textColor
                    x: dialogsName.x
                    y: parent.height / 3 * 2 - height / 2
                }

                Item {
                    id: imageCircle
                    x: 10
                    height: parent.height
                    width: height//parent.width / 4 - 20
                    y: parent.height / 2 - height / 2
                    Image {
                        id: profileImage
                        source: data_dir + "/Pictures/Profiles/" + chat_identification + ".jpg"
                        asynchronous: true
                        sourceSize: Qt.size(parent.width, parent.height)
                        smooth: true
                        visible: false
                    }
                    Image {
                        id: mask
                        source: "icons/circle.png"
                        sourceSize: Qt.size(parent.width, parent.height)
                        smooth: true
                        visible: false
                    }
                    OpacityMask {
                        anchors.fill: profileImage
                        source: profileImage
                        maskSource: mask
                    }
                }

                Label {
                    id: dialogsName
                    text: name
                    x: imageCircle.x + imageCircle.width * 1.5//window.width / 2 - width / 2
                    //y: parent.height / 2 - height / 2
                    y: parent.height / 3 - height / 2
                    font.pixelSize: mainWindow.width / 20
                    color: vars.textColor
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
