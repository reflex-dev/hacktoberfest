import reflex as rx
import state
from typing import List,Dict




def merged():
    return rx.center(
        
        "merged",
        font_size="14px",
        border_radius="13px",
        color="white",
        display="inline-block",
        padding="3px",
        bg="#00cec9",
        
    )


    
def not_merged():
    return rx.center(
        
        
        
    )

def merged_comp(pr :dict):
    return rx.cond(pr["merged"]==True,merged(),not_merged())
    

def menu_comp(pr :Dict[str,any]):
    return rx.popover(
        rx.popover_trigger(
            rx.button(
                "info",
                size="xs",
                color_scheme="teal",
                
            ),
            
            
        ),
        rx.popover_content(
        rx.popover_header(rx.center(rx.image(src=pr["avatar_url"],h="50px",w="50px",border_radius="25px",margin="6px",),rx.text(pr["author"])),),
        rx.popover_body(
            
           rx.vstack(
           rx.center(f"created at : {pr['created_at']}",
                     
                     
            ),
           rx.center(rx.link(
               pr["link"],
               href=f"{pr['link']}",
               color="#1e3799",
               font_size="15px",
               
           )),
           ),
            
            
        ),
        rx.popover_close_button(),
        ),
         
    )
   


    
def pull_no_comp(pr: Dict[str,str]):
    
    return rx.center(
        pr['pull_no'],
        bg="#f9ca24",
        font_size="15px",
        border_radius="2px",
        color="white",
        display="inline-block",
        padding="3px",
        
        
    )


def title(pr :dict):
    return rx.center(
        pr['title'],
        bg="#6c5ce7",
        font_size="20px",
        border_radius="13px",
        color="white",
        display="inline-block",
        padding="3px",
        margin="8px",
    )

def assigned():
    return rx.center(
        "assigned",
        bg="#78e08f",
        color="white",
        font_size="14px",
        border_radius="4px",
        display="inline-block",
        padding="3px"
    )
    
def not_assigned():
    return rx.center(
        
        "unassigned",
        bg="#18dcff",
        font_size="14px",
        border_radius="4px",
        color="white",
        display="inline-block",
        padding="3px",
        
    )
    
def approved():
    return rx.center(
        
        "approved",
        bg="#2ed573",
        font_size="14px",
        border_radius="4px",
        color="white",
        display="inline-block",
        padding="3px",
        
        
    )
    
    
def not_approved():
    return rx.center(
        "unapproved",
        bg="#ff4d4d",
        color="white",
        font_size="14px",
        border_radius="4px",
        display="inline-block",
        padding="3px",
        
    )
    
    
def status_open():
    return rx.center(
        
        "open",
        bg="#4cd137",
        font_size="14px",
        border_radius="4px",
        display="inline-block",
        color="white",
        padding="3px",
    )
    
    
def status_closed():
    return rx.center(
        "closed",
        bg="#e84118",
        font_size="14px",
        border_radius="4px",
        display="inline-block",
        color="white",
        padding="3px",
        
    )
    
    
def assigned_com(pr :dict):
    return rx.cond(pr["assigned"]==True,assigned(),not_assigned())

def approval_com(pr :dict):
    return rx.cond(pr["is_approved"]==True,approved(),not_approved())

def status_comp(pr :dict):
    return rx.cond(pr["status"]=="open",status_open(),status_closed())



    


def index():
    return rx.box(
        
        
        
        
        rx.vstack(
            rx.image(
            
            src="4373152_github_logo_logos_icon.png",
            h="200px",
            w="200px",
            margin_bottom="100px",
            
        ),
            
            rx.input(
                placeholder=f"enter your github access token...",
                value=state.app_state.token,
                on_change=state.app_state.set_token,
                font_size="20px",
                color="red",
                box_shadow= "0  3px 2px  grey",
                w="60%",
            ),
            rx.input(
                placeholder="enter repo name...",
                value=state.app_state.repo_name,
                on_change=state.app_state.set_repo_name,
                font_size="20px",
                color="red",
                box_shadow= "0  3px 2px  grey",
                w="60%",
                
            
            ),
            rx.input(
                placeholder="repo_owner name",
                value=state.app_state.user_name,
                on_change=state.app_state.set_user_name,
                font_size="20px",
                color="red",
                box_shadow= "0  3px 2px  grey",
                w="60%",
                
                
            ),
            
           
            rx.button(
                "get_prs",
                color_scheme="teal",
                on_click=state.app_state.return_pull_request_info,
                size="md"
                
                
                
            ),
            rx.menu(
                rx.menu_button(
                    "filter",
                ),
                rx.menu_list(
                    rx.menu_item("only merged prs",on_click=state.app_state.filter("only merged prs")),
                    rx.menu_item("approved prs",on_click=state.app_state.filter("approved prs")),
                    rx.menu_item("unassigned prs",on_click=state.app_state.filter("unassigned prs")),
                    rx.menu_item("open prs",on_click=state.app_state.filter("open prs")),
                    rx.menu_item("closed prs",on_click=state.app_state.filter("closed prs")),
                ),
                
            ),
           
            
            
            
            margin_bottom="40px",
            
        ),
        rx.box(
        rx.vstack(
            
            rx.foreach(state.app_state.data,
            lambda p:
                rx.hstack(
                title(p),
                assigned_com(p),
                status_comp(p),
                approval_com(p),
                pull_no_comp(p),
                merged_comp(p),
                menu_comp(p),
                
                
                
        ),
                
            ),
        ),
        box_shadow=" 0 7px 10px grey",
        h="90vh",
        w="70vw",
        overflow="auto",
        bg="white",
        position="relative",
        left="250px",
        margin="20px",
        border_radius="12px",
              
        ),
        
        
       
        w="100%",
        h="100vh",
        bg="white",
    
        overflow="scroll",
        
        
    )
        
    
    
    
app = rx.App()
app.add_page(index)
app.compile()

