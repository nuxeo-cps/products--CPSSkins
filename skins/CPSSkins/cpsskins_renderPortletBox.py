<div tal:attributes="class python: 'BoxColor%s BoxShape%s' % (here.boxcolor, here.boxshape)">
  <div tal:define="portlet nocall:options/portlet;
                   rendered options/rendered;
                   boxedit options/boxedit|nothing;
                   state portlet/getState;
                   portlet_url portlet/getURL;
                   boxlayout here/boxlayout;
                   boxlayout python: boxedit and 'portlet_edit' or boxlayout;
                   boxlayout_macro_path here/cpsskins_BoxLayouts/macros/?boxlayout|here/cpsskins_BoxLayouts/macros/standard"
       tal:attributes="style string:padding:${here/padding}">
    <metal:block use-macro="boxlayout_macro_path">
      <metal:block fill-slot="box_title" >
        <tal:block content="structure portlet/getTitle" />
      </metal:block>
      <metal:block fill-slot="box_body" >
        <tal:block content="structure rendered" />
      </metal:block>
    </metal:block>
  </div>
</div>
