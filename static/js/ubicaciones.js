function get_municipios(){
    new Ajax.Request('/coldeportes/entidad/buscarmunicipios', { 
    method: 'POST',
    parameters: $H({'type':$('id_type').getValue()}),
    onSuccess: function(transport) {
        var e = $('id_municipio')
        if(transport.responseText)
            e.update(transport.responseText)
    }
    }); // end new Ajax.Request
}