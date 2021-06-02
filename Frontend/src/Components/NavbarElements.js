import styled from 'styled-components';

export const Nav = styled.nav`
    background: #000;
    height:80px;
    // margin-top: -80px;
    display: flex;
    justify-content: centre;
    align-items: centre;
    font-size: 1rem;
    position: sticky;
    top:0;
    z-index: 10;

    @media screen and(max-width: 960px){
        transition: 0.8s all ease;
    }
`
export const NavbarContainer = styled.div`
    display: flex;
    justify-content: space-between;
    height: 80px;
    z-index: 1;
    width: 100%
    padding: 0 24px;
    maxwidth: 1100px;
`

export const NavLogo = styled.div`
    color: #fff;
    justify-self: flex-start;
    cursor: pointer;
    font-size: 1.5rem;
    font-weight: bold;
    display: flex;
    align-items: centre;
    margin-left: 24px;
    text-decoration: none;
`