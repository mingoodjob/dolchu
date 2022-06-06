$(document).ready(function () {

    $("#m_storelist").show()
    $("#d_storelist").hide()

    $("#m_list").click(function () {

        $("#m_storelist").show()
        $("#d_storelist").hide()
    })

    $("#d_list").click(function () {
        
        $("#m_storelist").hide()
        $("#d_storelist").show()

    })

})