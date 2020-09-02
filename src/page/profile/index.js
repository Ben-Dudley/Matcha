import React from 'react'
//import PropTypes from 'prop-types'


//TODO: переход на профиль .../matcha/profile/name_user
//TODO: нужен ли класс
class Profile extends React.Component {
    render() {
        return (<>
        {/* TODO: запрос пользователя */}
        <header>{'Серый волк, 25'}</header>
        <p>{'м, гей'}</p>
        <p>{'ЮЗАО Москва'}</p>
        <img src='volk.jpg' alt=""/>
        <p>{'Рейтинг славы: 10000000000000000'}</p>
        <p>{'О себе: в поисках своего зайца'}</p>
        <p>{'Мультипликация, животные, кулинария'}</p>
        </>)    
    }
}

export default Profile